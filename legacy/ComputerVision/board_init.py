import cv2
import sys
import numpy as np

OFFSET = 200
i = 0 

def crop(img, offset, show): 
    global i
    height = img.shape[0]
    width  = img.shape[1]
    center_x = int(width/2)
    center_y = int(height/2)
    
    cropped_image = img[center_y-offset:center_y+(offset), center_x-offset:center_x+(offset)]

    if not show:
        cv2.imwrite('example/' + str(i) + ".jpg", cropped_image)
        i += 1
        return crop
    cv2.imshow("frame", cropped_image)


def draw_crosshairs(img, offset, color):
    height = img.shape[0]
    width  = img.shape[1]
    center_x = int(width/2)
    center_y = int(height/2)

    copy = img.copy()
    #                     x       y
    cv2.drawMarker(copy, (center_x, center_y), color, markerType=cv2.MARKER_CROSS, thickness=2)
    cv2.drawMarker(copy, (center_x-offset, center_y-offset), color, markerType=cv2.MARKER_CROSS, thickness=2)
    cv2.drawMarker(copy, (center_x+offset, center_y-offset), color, markerType=cv2.MARKER_CROSS, thickness=2)
    cv2.drawMarker(copy, (center_x+offset, center_y+offset), color, markerType=cv2.MARKER_CROSS, thickness=2)
    cv2.drawMarker(copy, (center_x-offset, center_y+offset), color, markerType=cv2.MARKER_CROSS, thickness=2)

    cv2.imshow('ch', copy)


# creates 64 square images that measure differences between prev and cur board squares
def isolate_squares(img, OFFSET):
    height = img.shape[0]
    width  = img.shape[1]
    # center_x = int(width/2)
    # center_y = int(height/2)
    

    arr = [ [img]*8 for i in range(8)]
    for i in range (8):
        for j in range (8):
             # /4 because 2*offset (because offset from center) / 8 because 8 columns/rows
            arr[i][j] = img[int(i*OFFSET/4):int((i+1)*OFFSET/4), int(j*OFFSET/4):int((j+1)*OFFSET/4)]
            arr[i][j] = cv2.GaussianBlur(arr[i][j], (5,5), 5) # last 5 seems to matter - this got it to be 1321347, 947200 for 00 vs 02 and 03 vs 05
            #cv2.imshow("cropped", arr[i][j])
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            cv2.imwrite('board_pics/'+str(i)+str(j)+'.jpg', arr[i][j])
    
    return arr


def identify_squares(old, new):
    diff = [[0.0]*8]*8
    max1 = 0
    max2 = 0
    max1i = -1
    max1j = -1
    maxji = -1
    max2j = -1
    for i in range (8):
        for j in range (8):
            err = cv2.subtract(old[i][j], new[i][j])
            diff[i*8 + j] = np.sum(err**2)
            if diff[i*8 + j] > max1:
                max2 = max1
                max1 = diff[i*8 + j]
                max12i = max1i
                max12j = max1j
                max1i = i
                max1j = j
            elif diff[i*8 + j] > max2:
                max2 = diff[i*8 + j]
                max2i = i
                max2j = j
            
    diff.sort()
    return (max1, max1i, max1j, max2, max2i, max2j)
    
# def main():
#     img = cv2.imread('test_data/1.jpg',cv2.IMREAD_COLOR)

#     height = img.shape[0]
#     width  = img.shape[1]
#     # center_x = int(width/2)
#     # center_y = int(height/2 )
    
#     # Choose crosshair that is the easiest to view against board
#     CROSSHAIR_COLOR = (100, 200, 100)
#     draw_crosshairs(img, 400, CROSSHAIR_COLOR)
#     # cropped_image =  img[center_y-OFFSET:center_y+OFFSET, center_x-OFFSET:center_x+OFFSET]
#     # cropped_image = crop(img, 400)
#     # cv2.imshow("cropped", cropped_image)

#     # arr = isolate_squares(cropped_image, OFFSET)
 
#     # cv2.imwrite('board_pics/cropped.jpg', cropped_image)

#     # err = cv2.subtract(arr[0][0], arr[0][2])
#     # err = np.sum(err**2)
#     # print(err)
#     # err = cv2.subtract(arr[0][3], arr[0][5])
#     # err = np.sum(err**2)
#     # print(err)

#     # cv2.imshow('align board with crosshairs', img)

#     # when you hit enter, it'll leave the image window
#     if cv2.waitKey(0) == 32:
#         CROSSHAIR_COLOR = (200, 100, 100)
#         draw_crosshairs(img, 400, CROSSHAIR_COLOR)
#         cv2.imwrite('board_pics/taken.jpg', img)
#         crop(img, 640)
#         cv2.imwrite('board_pics/cropped.jpg', img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

def main():
    vid = cv2.VideoCapture(0)
    offset = 240
    while(True):
        ret, f = vid.read()
        # crop(f)
        CROSSHAIR_COLOR = (100, 100, 250)
        
        print(offset)

        draw_crosshairs(f, offset, CROSSHAIR_COLOR)
        # cv2.imshow('frame', f)
        # if frame:
            # frame(f)
        crop(f,offset,True)
        x = cv2.waitKey(1)
        if x & 0xFF == ord('q'):
            break
        if x & 0xFF == ord('w'):
            print("Hello!")
            offset += 1
        if x & 0xFF == ord('s'):
            offset -= 1
        if x & 0xFF == ord('s'):
            offset -= 1
        # if x & 0xFF == ord('t'):
        if x & 0xFF == ord('m'):
            crop(f, offset, False)

if __name__ == '__main__':
    main()