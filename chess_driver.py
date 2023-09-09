import argparse
import cv2
from vision.board_vision import BoardVision
import vision.chess_conversions as cc
import ai.ai as ai
import chess.svg
import web.webapp as webapp
import arm
import numpy as np
from threading import Thread
import base64
import chess
import os
import time

white = ""
black = ""
arm_exists = True

CONFIDENCE_THRESHOLD = 1.2

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    

def stream_img(name, img):
    _, buffer = cv2.imencode('.jpg', img)
    base64_str = base64.b64encode(buffer).decode()
    # webapp.push_message("cv2", name, base64_str)


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


    most_likely_legal_move = move_scores[0][1]
    most_likely_legal_score = move_scores[0][0]

    # print("selected move:: ", most_likely_legal_move, "\n")
    castling = game.is_castling(most_likely_legal_move)
    if castling:
        castling = cc.get_castle_squares(str(most_likely_legal_move))

    # append all differences and their positions to a list
    squareList = []
    i = 0
    while i < 64:
        squareList.append([diffs[i//8][i%8], i//8, i%8])
        i+=1

    squareList = sorted(squareList)
    most_likely_any_score = squareList[-1][0] + squareList[-2][0]

    # if most_likely_any_score > CONFIDENCE_THRESHOLD * most_likely_legal_score:
        # return False

    return most_likely_legal_move, castling, game.san(most_likely_legal_move), move_scores[0][0]/sum_scores


def start_game(src):
    bv = BoardVision(src)   
   
    board = chess.Board()
    robots_turn = True

    if arm_exists:
        arm.instantiateArm()
        arm.calibrate(unsafe=False, robot_known_white= 'W' if robots_turn else 'B')
        arm.rotate()

    print("calibration complete....")

    time.sleep(3)

    print('start arm done')

    # web = Thread(target=webapp.start, args =())
    # web.start()
    # webapp.push_message("cls", "")

    clear()
    while True:

        best_move = ai.getMove(board.fen())
        board_eval = ai.getEval()
        
        print(f"board eval: {board_eval}")
        print(f"best next move: {best_move}")
        print("\ncurrent position: ")
        ai.boardPrint()

        # capture pre-move position
        before = bv.capture()
        if not type(before) == np.ndarray:
            break
        cv2.waitKey(1)
        # stream_img("raw", before)

        is_capture = False
        is_ep = False
        
        # wait for next move / other instruction from webapp
        # req = webapp.await_message()

        # if robots turn, take robot's command, otherwise take human command
        if robots_turn:
            req = "MOVE " + best_move[:2] + " " + best_move[2:]
            best_move_as_Move = chess.Move.from_uci(best_move)
            is_capture = board.is_capture(best_move_as_Move)
            is_ep = board.is_en_passant(best_move_as_Move)
            is_castling = board.is_castling(best_move_as_Move)
            if is_ep:
                print("EN PASSSSSSSSSANT")
                is_ep = board.ep_square
                is_ep = chess.square_name(is_ep)
            if is_capture:
                print("move is a capture!!! yikes")
            if is_castling:
                other_squares = cc.get_castle_squares(best_move)
                req += " " + other_squares[:2] + " " + other_squares[2:]
        else:
            req = input("press ENTER on move, or command: ")


        # command parsing
        force_move = False
        reqSplit = req.split(" ")
        if reqSplit[0].upper() == "HALT" or reqSplit[0].upper() == "Q":
            print('quitting...')
            # web.join()
            break
        if reqSplit[0].upper() == "MOVE":
            if len(reqSplit) < 3:
                print("ERROR: NOT ENOUGH PARAMS IN MOVE (EXPECTED 3) + ", reqSplit)
                break;
            force_move = reqSplit[1] + reqSplit[2]

            if arm_exists:
                capture_square = ""
                if is_capture:
                    capture_square = reqSplit[2] if not is_ep else is_ep
                if is_ep:
                    capture_square = reqSplit[2][:1]
                    if arm.Arm_constants.ROBOT_COLOR:
                        capture_square+=str(int(reqSplit[2][1:]) + 1)
                    else:
                        capture_square+=str(int(reqSplit[2][1:]) - 1)
                print(reqSplit)
                arm.movePieceAndRotate(reqSplit[1], reqSplit[2], capture_square)
                if len(reqSplit) == 5:
                    arm.movePieceAndRotate(reqSplit[3], reqSplit[4])
        if reqSplit[0] == "": # move 
            print("getting next")


        # capture position after move
        after = bv.capture(no_inc=True)
        if not type(after) == np.ndarray:
            break
        cv2.imshow("current", after)

        # compare move to previous position
        difference = bv.subtract_pos(before, after)
        difference_grid = bv.rescale_grid(difference)
        likely_move  = get_likely_move(board, difference_grid)

        # checks for likely move being legal
        if likely_move:
            move, castling, san, prob = likely_move
        # else:
        #     print("illegal move detected!!")
        #     _ = input("undo move and press ENTER before correcting") 
        #     continue

        if force_move:
            move = force_move
            san = board.san(chess.Move.from_uci(move))
            print(f"insan {san}")
        message = f"{str(move)[0:2]}-{str(move)[2:4]}"
        if castling:
            message += " O-O " + castling[0:2] + "-" + castling[2:4]

        clear()
        print("---------------------------")
        verb = "detected by camera" if not force_move else "made by arm"
        print(f"move {verb}: {str(san)}")

        # webapp.push_message("mov", str(message))
        # webapp.push_message("san", str(san))
        # webapp.push_message("prb", str(prob))
        # cv2.imshow("difference", difference)
        # stream_img("diff", difference)

        # updates board state
        board.push_uci(str(move))
        
            
        robots_turn = not robots_turn


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
    # if args.black not in ['H', 'R_ARM', 'H_ARM']:
    #     raise ValueError('black must be H, R_ARM or H_ARM')
    
    white = args.white
    black = args.black
    
    start_game(args.src)

if __name__ == "__main__":
    main()