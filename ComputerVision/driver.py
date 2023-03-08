import cv2
import sys
import os
import numpy as np
from board_vision import BoardVision
from chessboard import Chessboard

SOURCE = "example/" 
FLAG = "IMG"
DEFAULT_CROSSHAIR_OFFSET = 240

frame_iterator = 0


def clear():
    """
    clears system console (os independent)
    for aesthetics
    """

    os.system('cls' if os.name == 'nt' else 'clear')


def validate_initial_detections(detection_grid):
    """ 
    determines if the initial detections_grid is valid,
    by ensuring it matches the starting position of a 
    chess game:  WHAT HAPPENED!! you kinda have to hang up for me to tell you
    X X X X X X X X
    X X X X X X X X
    - - - - - - - -
    - - - - - - - -
    - - - - - - - -
    - - - - - - - -
    X X X X X X X X
    X X X X X X X X 

    """

    for i in range(8):
        if not all(val == ('X' if i < 2 or i > 5 else '-') for val in detection_grid[i]):
            valid_row = ['X' if i < 2 or i > 5 else '-' for j in range(8)]
            return False, f"ROW {i} INVALID \n{detection_grid[i]} != {valid_row}"
    return True, None


def get_frame(cap, increment=True):
    global frame_iterator
    if cap == "IMG":
        frame = cv2.imread('test_data/' + frame_iterator + '.jpg',cv2.IMREAD_COLOR)
        frame_iterator += 1 if increment else 0
        return frame
    ret, frame = cap.read()
    return frame

def align_board(img, offset):
    """
     (x1,y1) ------|  
     | ------(x2,y2)
    """

    print("\nalign board with 4 green crosshairs\npress ENTER to continue ...")
   
    height = img.shape[0]
    width  = img.shape[1]
    center_x = int(width/2)
    center_y = int(height/2)

    copy = img.copy()
    color = (200, 100, 100)

    #                     x       y
    cv2.drawMarker(copy, (center_x, center_y), color, markerType=cv2.MARKER_CROSS, thickness=2)
    cv2.drawMarker(copy, (center_x-offset, center_y-offset), color, markerType=cv2.MARKER_CROSS, thickness=2)
    cv2.drawMarker(copy, (center_x+offset, center_y-offset), color, markerType=cv2.MARKER_CROSS, thickness=2)
    cv2.drawMarker(copy, (center_x+offset, center_y+offset), color, markerType=cv2.MARKER_CROSS, thickness=2)
    cv2.drawMarker(copy, (center_x-offset, center_y+offset), color, markerType=cv2.MARKER_CROSS, thickness=2)

    cv2.imshow('crosshair window', copy)
    
    return (center_x-offset, center_x+offset, center_y-offset, center_y+offset)

def get_alignment(cap):
    global offset
    while(True):
        frame = get_frame(cap, increment=False)
        
        print(offset)
        
        draw_crosshairs(frame, offset, CROSSHAIR_COLOR)
        crop(frame,offset,True)

        x = cv2.waitKey(1)
        if x == 32:
            return align_board(frame, offset)
        if x & 0xFF == ord('w'):
            print("Hello!")
            offset += 1
        if x & 0xFF == ord('s'):
            offset -= 1
        if x & 0xFF == ord('s'):
            offset -= 1
        if x & 0xFF == ord('m'):
            crop(f, offset, False)


def main():
    clear()

    vision, err = BoardVision()
    board = Chessboard()

    cap = cv2.VideoCapture(0) if FLAG=="CAM" else "IMG"

    board_points = align_board(a)

    detection_grid, err = vision.capture_position()
    if err:
        print("Error generating detection grid: " + err)

    valid, err = validate_initial_detections(detection_grid)
    if err:
        print("Error validating initial board: " + err)
    

    while True:
        clear()
        
        print("vision driver | board projection\n")
        print(board)
        print(board.get_fen())

        input("\nmake move and press ENTER to continue...")

        #




if __name__ == '__main__':
    main()