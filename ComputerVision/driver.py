import cv2
import sys
import os
import numpy as np
import board_controller as bc
from board import Board


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    clear()
    cap = cv2.VideoCapture(0)

    print("vision driver | initialize board")
    # crop, tracking_coords = bc.align_board(cap) # tracking coords ignored for now
    

    board = Board((1,2,3,4))
    print(board)

    while True:
        clear()
        
        print("vision driver | board projection\n")
        print(board)

        input("\make move and press ENTER to continue...")




if __name__ == '__main__':
    main()