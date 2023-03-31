import cv2
import os
import numpy as np
import time

CROSSHAIR_COLOR = (100, 100, 250)

def crop(img, offset, show): 
    global i
    height = img.shape[0]
    width  = img.shape[1]
    center_x = int(width/2)
    center_y = int(height/2)
    
    coords = [center_y-offset,center_y+(offset),center_x-offset,center_x+(offset)]
    return img[center_y-offset:center_y+(offset), center_x-offset:center_x+(offset)], coords


def draw_crosshairs(img, offset, color):
    height = img.shape[0]
    width  = img.shape[1]
    center_x = int(width/2)
    center_y = int(height/2)

    copy = img.copy()

    #                     x         y
    cv2.drawMarker(copy, (center_x, center_y), color, markerType=cv2.MARKER_CROSS, thickness=2)
    cv2.drawMarker(copy, (center_x-offset, center_y-offset), color, markerType=cv2.MARKER_CROSS, thickness=2)
    cv2.drawMarker(copy, (center_x+offset, center_y-offset), color, markerType=cv2.MARKER_CROSS, thickness=2)
    cv2.drawMarker(copy, (center_x+offset, center_y+offset), color, markerType=cv2.MARKER_CROSS, thickness=2)
    cv2.drawMarker(copy, (center_x-offset, center_y+offset), color, markerType=cv2.MARKER_CROSS, thickness=2)

    return copy

class BoardVision:
    def __init__(self, src):
        self.using_images = (src != "CAM")
        self.frame_iterator = 0
        self.src = src
        self.curr_cap = False

        if self.using_images:
            print(f"alternate src detected: {src}")
            print("using image mode...")
        else:
            print("initializing camera...")
            self.cap = cv2.VideoCapture(0)
            while not self.cap.isOpened():
                print("waiting for cam")
                cv2.waitKey(1000)  # Wait for 1 second
            print("has camera!")
            self.board_coords = self.ident_board()


    def ident_board(self):
        offset = 240
        while(True):
            _, frame = self.cap.read()

            crosshairs = draw_crosshairs(frame, offset, CROSSHAIR_COLOR)
            cv2.imshow("crosshairs | w - increase, s  - decrease, enter - confirm", crosshairs)

            raw, coords = crop(frame,offset,True)
            cv2.imshow("output view", raw)

            inp = cv2.waitKey(1)
            key = inp & 0xFF
            if key == ord('q'):
                break
            if key == ord('w'):
                offset += 1
            if key == ord('s'):
                offset -= 1
            if key == 13:
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                cv2.waitKey(1)
                cv2.waitKey(1)
                cv2.waitKey(1)
                return coords
        return False

    def capture_from_img(self):
        path = f"{self.src}/" + str(self.frame_iterator) + '.jpg'
        if not os.path.exists(path):
            return False
        res = cv2.imread(path, cv2.IMREAD_COLOR)
        self.curr_cap = cv2.rotate(res, cv2.ROTATE_90_CLOCKWISE)
        self.frame_iterator += 1
        return self.curr_cap

    def capture(self):
        self.last_cap = self.curr_cap
        if self.using_images:
            return self.capture_from_img()
        _, raw = self.cap.read()
        coords = self.board_coords
        if not type(coords) == list:
            return False
        crop = raw[coords[0]:coords[1], coords[2]:coords[3]]
        self.curr_cap = cv2.rotate(crop, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return self.curr_cap

    def subtract_pos(self):
        side = int(self.last_cap.shape[0]/8)
        if not type(self.last_cap) == np.ndarray:
            return False
        
        kernel = np.array([[0, 2, 0],
                          [2, 0, 2],
                          [0, 2, 0]])

        white_curr = self.curr_cap
        white_last = self.last_cap
        black_curr = cv2.filter2D(src=white_curr, ddepth=-1, kernel=kernel)
        black_last = cv2.filter2D(src=white_last, ddepth=-1, kernel=kernel)
        color = (255, 0, 0)

        # return cv2.absdiff(black_curr, black_last)

        white_diff = cv2.absdiff(white_curr, white_last)
        total_diff = white_diff.copy()

        black = False
        for r in range(8):
            black = r % 2 != 0
            for c in range(8):
                curr = black_curr if black else white_curr
                last = black_last if black else white_last

                sub_curr = curr[(side*r):((side*r)+side), (side*c):((side*c)+side)]
                sub_last = last[(side*r):((side*r)+side), (side*c):((side*c)+side)]
                sub_diff = cv2.absdiff(sub_curr, sub_last)
                # sub_diff = cv2.rectangle(sub_diff, (1, 1),(side-1, side-1), color, 2) if black else sub_diff

                total_diff[(side*r):(side*r)+sub_diff.shape[0], (side*c):(side*c)+sub_diff.shape[1]] = sub_diff
                black = not black
        return total_diff
    
    def rescale_grid(self, img):
        side = int(img.shape[0]/8)
        res = [ [0]*8 for i in range(8)]
        for r in range (8):
            for c in range (8):
                sub_image = img[(side*r):((side*r)+side), (side*c):((side*c)+side)]
                total_value = cv2.sumElems(sub_image)
                total_value = total_value[0] + total_value[1] + total_value[2]  
                res[r][c] = total_value
        return res

    def track_board():
        pass

