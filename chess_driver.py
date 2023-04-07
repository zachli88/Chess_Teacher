import argparse
import cv2
from vision.board_vision import BoardVision
import vision.chess_conversions as cc
import web.webapp as webapp
import arm
import numpy as np
from threading import Thread
import base64
import chess
import os

white = ""
black = ""


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    

def stream_img(name, img):
    _, buffer = cv2.imencode('.jpg', img)
    base64_str = base64.b64encode(buffer).decode()
    webapp.push_message("cv2", name, base64_str)


def get_likely_move(game, diffs):
    move_scores = []
    board_sum = 0
    for move in game.legal_moves:
        f_r, f_c = cc.uci_to_position(chess.square_name(move.from_square))
        from_sum = diffs[f_r][f_c]
        t_r, t_c = cc.uci_to_position(chess.square_name(move.to_square))
        to_sum = diffs[t_r][t_c]
        if(game.is_castling(move)):
            move_sum = (from_sum + to_sum + cc.castle_sums(str(move), diffs))
        else:
            move_sum = from_sum+to_sum
            board_sum += move_sum
        move_scores.append([move_sum, move, f_r, f_c, t_r, t_c])
    move_scores = sorted(move_scores, reverse=True, key=lambda x: x[0])

    num_elements_to_sum = min(3, len(move_scores))
    sum_scores = sum(score for score, _, _, _, _, _ in move_scores[:num_elements_to_sum])


    selected_move = move_scores[0][1]
    castling = game.is_castling(selected_move)
    if castling:
        castling = cc.get_castle_squares(str(selected_move))

    return selected_move, castling, game.san(selected_move), move_scores[0][0]/sum_scores


def start_game(src):
    bv = BoardVision(src)   
   
    board = chess.Board()

    # arm.instantiateArm()
    # arm.calibrate()
    # arm.rotate()

    web = Thread(target=webapp.start, args =())
    web.start()
    webapp.push_message("cls", "")

    white = True

    while True:
        # capture pre-move position
        before = bv.capture()
        if not type(before) == np.ndarray:
            break
        stream_img("raw", before)


        # wait for next move / other instruction from webapp
        req = webapp.await_message()
        force_move = False
        reqSplit = req.split(" ")
        if reqSplit[0] == "HALT":
            print('quitting...')
            web.join()
            break
        if reqSplit[0] == "MOVE":
            if len(reqSplit) < 3:
                print("ERROR: NOT ENOUGH PARAMS IN MOVE (EXPECTED 3) + ", reqSplit)
                break;
            force_move = reqSplit[1] + reqSplit[2]
            print("making move")
        if reqSplit[0] == "NEXT": # move 
            print("getting next")
        print(req)


        # capture position after move
        after = bv.capture(no_inc=True)
        if not type(after) == np.ndarray:
            break
        stream_img("diff", after)

        # compare move to previous position
        difference = bv.subtract_pos(before, after)
        difference_grid = bv.rescale_grid(difference)
        move, castling, san, prob  = get_likely_move(board, difference_grid)
        if force_move:
            move = force_move
        message = f"{str(move)[0:2]}-{str(move)[2:4]}"
        if castling:
            message += " O-O " + castling[0:2] + "-" + castling[2:4]

        print(move)

        webapp.push_message("mov", str(message))
        webapp.push_message("san", str(san))
        webapp.push_message("prb", str(prob))

        board.push_uci(str(move))
        stream_img("diff", difference)
            
        white = not white


def main():
    global white
    global black
    
    parser = argparse.ArgumentParser(description='robot arm that plays chess')
    parser.add_argument('-w', '--white', type=str, required=True, metavar="PLAYER",
                        help='specify who plays white (H , R_ARM , or H_ARM)')
    parser.add_argument('-b', '--black', type=str, required=True, metavar="PLAYER",
                        help='specify who plays black (H , R_ARM, or H_ARM)')
    parser.add_argument('--src', type=str, metavar="'/image_dir'",
                        help='specify source image directory', default="CAM")
    parser.add_argument('-tc', '--time-control', type=str, default='NONE', metavar="10/2",
                    help='time control for the game in the format <minutes>/<increment> (e.g. 10/2 for 10 minutes with a 2 second increment). If not specified, the game will have no time control.')


    args = parser.parse_args()
    if args.white not in ['H', 'R_ARM', 'H_ARM']:
        raise ValueError('white must be H, R_ARM, H_ARM')
    if args.black not in ['H', 'R_ARM', 'H_ARM']:
        raise ValueError('black must be H, R_ARM or H_ARM')
    
    white = args.white
    black = args.black
    
    start_game(args.src)

if __name__ == "__main__":
    main()