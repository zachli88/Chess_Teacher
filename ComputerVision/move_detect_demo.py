import cv2
import sys
import numpy as np
import webapp
import threading
from flask_socketio import SocketIO, emit
import chess


def highlight_rect(img, r, c, color):
    side = int(img.shape[0]/8)

    start_point = ((side*r)+1, (side*c)+1)
    end_point = ((side*r)+side-1, (side*c)+side-1)
  
    

    thickness = 1

    # Using cv2.rectangle() method
    # Draw a rectangle with blue line borders of thickness of 2 px
    img = cv2.rectangle(img, start_point, end_point, color, thickness)
    return img

def get_diffs(img):
    side = int(img.shape[0]/8)
    diffs = [ [0]*8 for i in range(8)]
    print("showing!!")
    for r in range (8):
        for c in range (8):
            sub_image = img[(side*r):((side*r)+side), (side*c):((side*c)+side)]
            total_value = cv2.sumElems(sub_image)
            total_value = total_value[0] + total_value[1] + total_value[2]  
            diffs[r][c] = total_value
            # cv2.imshow(f"{r},{c} = {total_value}", sub_image)
            # cv2.waitKey(0)

    return diffs

def grid(img, diffs):
    maximum = np.amax(diffs)

    np_diffs = np.array(diffs)
    most_moved = np.argmax(np_diffs)
    first_pos = np.unravel_index(most_moved, np_diffs.shape)
    print(first_pos)
    np_diffs[first_pos] = 0

    second_most_moved = np.argmax(np_diffs)
    second_pos = np.unravel_index(second_most_moved, np_diffs.shape)
    print(second_pos)

    for row in range(8):
        for col in range(8):
            # fractional = diffs[row][col]/maximum
            color = (255, 0, 0)
            coords = (row, col)
            if (coords == first_pos):
                color = (0,255,0)
            if (coords == second_pos):
                color = (0,165,265)
            img = highlight_rect(img, col, row, color)
    return img, first_pos, second_pos

def position_to_uci(position):
    row, col = position
    

    uci_col = chr(ord('a') + col)
    uci_row = str(8 - row)
    
    return uci_col + uci_row

i = 0
img_before = cv2.imread(f'example/{i}.jpg',cv2.IMREAD_COLOR)
img_after = cv2.imread(f'example/{i+1}.jpg',cv2.IMREAD_COLOR)

contrast = 1. # Contrast control ( 0 to 127)
brightness = 10. # Brightness control (0-100)


cv2.imshow("raw", img_before)
cv2.imshow("detect", img_after)
cv2.moveWindow("detect", img_after.shape[0]+20,-1000) 

x = threading.Thread(target=webapp.start, args=())
x.start()

cv2.waitKey(0)



board = chess.Board()


while True:
    img_before = cv2.imread(f'example/{i}.jpg',cv2.IMREAD_COLOR)
    img_after = cv2.imread(f'example/{i+1}.jpg',cv2.IMREAD_COLOR)


    img_before = cv2.GaussianBlur(img_before, (5,5), 3)
    img_after = cv2.GaussianBlur(img_after, (5,5), 3)
    img_before = cv2.addWeighted( img_before, contrast, img_before, 0, brightness)
    img_after = cv2.addWeighted( img_after, contrast, img_after, 0, brightness)


    img_diff = cv2.absdiff(img_after,img_before)
    img_diff =cv2.rotate(img_diff, cv2.ROTATE_90_CLOCKWISE)
    img_after =cv2.rotate(img_after, cv2.ROTATE_90_CLOCKWISE)
    img_diff = cv2.convertScaleAbs(img_diff, alpha=2.0, beta=0)
    img_diff = cv2.addWeighted( img_diff, contrast, img_diff, 0, brightness)


    diffs = get_diffs(img_diff)
    img_diff, first, second = grid(img_diff, diffs)

    first = position_to_uci(first)
    second = position_to_uci(second)

    if chess.Move.from_uci(f"{first}{second}") in board.legal_moves:
        print(f"identified move == {first}{second}")
        board.push_uci(f"{first}{second}")
        webapp.update_data(f"{first}-{second}")
    elif chess.Move.from_uci(f"{second}{first}") in board.legal_moves:
        board.push_uci(f"{second}{first}")
        print(f"identified move == {second}{first}")
        webapp.update_data(f"{second}-{first}")
    else:
        print(f"identified move == NONE")
        webapp.update_data("NA")
    
    
        

    # add text to the image
    text = str(i+1) + ". " 
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 1
    thickness = 2
    color = (0, 0, 255) # BGR color tuple
    position = (50, 50) # x, y coordinates


    cv2.putText(img_diff, text, position, font, font_scale, color, thickness)
    cv2.imshow("raw", img_after)
    cv2.imshow("detect", img_diff)


    key_press = cv2.waitKey(0) & 0xFF
    if key_press == ord('d'):
        print("incrementing...")
        i+=1
    elif key_press == ord('a'):
        print("decrementing...")
        i-=1
    elif key_press == ord('q'):
        x.eq
        break
    else:
        print("ok!")