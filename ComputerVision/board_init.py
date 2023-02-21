import cv2
import sys
import numpy as np

OFFSET = 400

def crop(img, offset): 
    height = img.shape[0]
    width  = img.shape[1]
    center_x = int(width/2)
    center_y = int(height/2)

    cropped_image = img[center_x-offset:center_x+2*offset][center_y-offset:center_y+2*offset]
    cv2.imshow("select corners", cropped_image)


def draw_crosshairs(img, offset, color):
    height = img.shape[0]
    width  = img.shape[1]
    center_x = int(width/2)
    center_y = int(height/2)

    copy = img.copy()
    #                     x       y
    cv2.drawMarker(copy, (center_x, center_y), color, markerType=cv2.MARKER_CROSS, thickness=4)
    cv2.drawMarker(copy, (center_x-OFFSET, center_y-OFFSET), color, markerType=cv2.MARKER_CROSS, thickness=4)
    cv2.drawMarker(copy, (center_x+OFFSET, center_y-OFFSET), color, markerType=cv2.MARKER_CROSS, thickness=4)
    cv2.drawMarker(copy, (center_x+OFFSET, center_y+OFFSET), color, markerType=cv2.MARKER_CROSS, thickness=4)
    cv2.drawMarker(copy, (center_x-OFFSET, center_y+OFFSET), color, markerType=cv2.MARKER_CROSS, thickness=4)

    cv2.imshow('align boardzzz with crosshairs', copy)


def main():
    img = cv2.imread('test_data/4.jpg',cv2.IMREAD_COLOR)
    
    
    CROSSHAIR_COLOR = (100, 200, 100)
    draw_crosshairs(img, 400, CROSSHAIR_COLOR)

    # cv2.imshow('align board with crosshairs', img)

    if cv2.waitKey(0) == 32:
        CROSSHAIR_COLOR = (200, 100, 100)
        draw_crosshairs(img, 400, CROSSHAIR_COLOR)
        cv2.imwrite('board_pics/taken.jpg', img)
        crop(img, 400)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()