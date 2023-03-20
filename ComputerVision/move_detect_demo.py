import cv2
import sys
import os
import numpy as np
import webapp
import threading
from flask_socketio import SocketIO, emit
import chess


def clear():
    """
    clears system console (os independent)
    for aesthetics
    """

    os.system('cls' if os.name == 'nt' else 'clear')

def highlight_rect(img, r, c, color):
    side = int(img.shape[0]/8)

    start_point = ((side*r)+1, (side*c)+1)
    end_point = ((side*r)+side-1, (side*c)+side-1)

    thickness = 1

    img = cv2.rectangle(img, start_point, end_point, color, thickness)
    return img

def get_diffs(img):
    side = int(img.shape[0]/8)
    diffs = [ [0]*8 for i in range(8)]
    for r in range (8):
        for c in range (8):
            sub_image = img[(side*r):((side*r)+side), (side*c):((side*c)+side)]
            total_value = cv2.sumElems(sub_image)
            total_value = total_value[0] + total_value[1] + total_value[2]  
            diffs[r][c] = total_value
    return diffs


def uci_to_position(uci_square):
    file, rank = uci_square[0], int(uci_square[1])
    row = 8 - rank
    col = ord(file) - ord('a')
    return row, col


def coord_sum(uci, diffs):
    r, c = uci_to_position(uci)
    return diffs[r][c]

def castle_sums(move, diffs):
    if move == "e8c8":
        return coord_sum("a8", diffs) + coord_sum("d8", diffs)
    elif move == "e1c1":
        return coord_sum("a1", diffs) + coord_sum("d1", diffs)
    elif move == "e8g8":
        return coord_sum("f8", diffs) + coord_sum("h8", diffs)
    elif move == "e1g1":
        return coord_sum("f1", diffs) + coord_sum("h1", diffs)
    return 0

def get_castle_squares(move):
    if move == "e8c8":
        return "a8d8"
    elif move == "e1c1":
        return "a1d1" 
    elif move == "e8g8":
        return "f8h8"
    elif move == "e1g1":
        return "f1h1"


def grid(img, diffs, board):
    maximum = np.amax(diffs)

    # np_diffs = np.array(diffs)
    # most_moved = np.argmax(np_diffs)
    # first_pos = np.unravel_index(most_moved, np_diffs.shape)
    # print(first_pos)
    # np_diffs[first_pos] = 0

    # second_most_moved = np.argmax(np_diffs)
    # second_pos = np.unravel_index(second_most_moved, np_diffs.shape)
    # print(second_pos)

    move_scores = []

    ultimate_sum = 0
    for move in board.legal_moves:
        f_r, f_c = uci_to_position(chess.square_name(move.from_square))
        from_sum = diffs[f_r][f_c]
        t_r, t_c = uci_to_position(chess.square_name(move.to_square))
        to_sum = diffs[t_r][t_c]
        if(board.is_castling(move)):
            print("CASTLING MOVE DETECTED!!! " + str(move))
            move_sum = (from_sum + to_sum + castle_sums(str(move), diffs))
        else:
            move_sum = from_sum+to_sum
            ultimate_sum += move_sum
        move_scores.append([move_sum, move, f_r, f_c, t_r, t_c])

    move_scores = sorted(move_scores, reverse=True, key=lambda x: x[0])
    selected_move = move_scores[0][1]
    castling = board.is_castling(selected_move)
        

    # print("possible moves::")
    # for i, m_s in enumerate(move_scores):
    #     print(f"{i}. {m_s[1]} - {((m_s[0]/ultimate_sum)*100.0):.2f}% - {'CASTLING' if board.is_castling(m_s[1]) else ''}")
    #     if i >= 5:
    #         break

    for row in range(8):
        for col in range(8):
            # fractional = diffs[row][col]/maximum
            color = (100, 100, 100)
            coords = (row, col)
            if (coords == (move_scores[0][2], move_scores[0][3])):
                color = (0,255,0)
            if (coords == (move_scores[0][4], move_scores[0][5])):
                color = (0,165,265)
            
            img = highlight_rect(img, col, row, color)

    if castling:
        castling = get_castle_squares(str(selected_move))
            
    return img, selected_move, castling#, first_pos, second_pos


def position_to_uci(position):
    row, col = position
    uci_col = chr(ord('a') + col)
    uci_row = str(8 - row)
    return uci_col + uci_row



i = 0
img_before = cv2.imread(f'example/{i}.jpg',cv2.IMREAD_COLOR)
img_after = cv2.imread(f'example/{i+1}.jpg',cv2.IMREAD_COLOR)
img_before =cv2.rotate(img_before, cv2.ROTATE_90_CLOCKWISE)
img_after =cv2.rotate(img_after, cv2.ROTATE_90_CLOCKWISE)

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
    img_diff, selected_move, castling = grid(img_diff, diffs, board)

    # first = position_to_uci(first)
    # second = position_to_uci(second)

    # if chess.Move.from_uci(f"{first}{second}") in board.legal_moves:
    #     print(f"identified move == {first}{second}")
    #     board.push_uci(f"{first}{second}")
    #     webapp.update_data(f"{first}-{second}")
    # elif chess.Move.from_uci(f"{second}{first}") in board.legal_moves:
    #     board.push_uci(f"{second}{first}")
    #     print(f"identified move == {second}{first}")
    #     webapp.update_data(f"{second}-{first}")
    # else:
    #     print(f"identified move == NONE")
    #     webapp.update_data("NA")
    clear()
    emission_data = f"{str(selected_move)[0:2]}-{str(selected_move)[2:4]}"
    if castling:
        emission_data += " O-O " + castling[0:2] + "-" + castling[2:4] 
    print(f"identified move == {selected_move} " + castling if castling else "")
    board.push_uci(str(selected_move))
    webapp.update_data(emission_data)
    print(board)
    
    
        

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