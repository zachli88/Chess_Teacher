import arm
import vision.chess_conversions as cc

# Moves piece on starting square to a given ending square
# inputs: starting_square to move from, ending_square to move to
# output: returns true on success, false on failure
def move_piece(starting_square: str, ending_square: str):
    #movePieceAndRotate
    arm.movePieceAndRotate(starting_square, ending_square, "")

def capture_piece(starting_square: str, ending_square: str):
    # capture part of move piece and rotate
    arm.movePieceAndRotate(starting_square, ending_square, "capture")

def castle(side: str):
    if (side == "king"):
        if (arm.Arm_constants.ROBOT_COLOR):
            move_piece("e8", "g8")
            move_piece("h8", "f8")
            move_piece("e1", "g1")
            move_piece("h1", "f1")
        else:
            move_piece("e8", "g8")
            move_piece("h8", "f8")
    elif (arm.Arm_constants.ROBOT_COLOR):
        move_piece("e1", "c1")
        move_piece("a1", "d1")
        
    else:
        move_piece("e8", "c8")
        move_piece("a8", "d8")

def en_passant(starting_square: str, direction: str):
    row, col = cc.uci_to_position(starting_square)
    if(arm.Arm_constants.ROBOT_COLOR):
        if(direction == "right"):
            newUCI = cc.position_to_uci(row + 1, col + 1)
            arm.movePiece(starting_square, newUCI)
            captureUCI = cc.position_to_uci(row, col + 1)
            remove(captureUCI)
        else:
            newUCI = cc.position_to_uci(row + 1, col - 1)
            arm.movePiece(starting_square, newUCI)
            captureUCI = cc.position_to_uci(row, col - 1)
            remove(captureUCI)
    else:
        if(direction == "right"):
            newUCI = cc.position_to_uci(row - 1, col - 1)
            arm.movePiece(starting_square, newUCI)
            captureUCI = cc.position_to_uci(row, col - 1)
            remove(captureUCI)
        else:
            newUCI = cc.position_to_uci(row - 1, col + 1)
            arm.movePiece(starting_square, newUCI)
            captureUCI = cc.position_to_uci(row, col + 1)
            remove(captureUCI)        


def remove(capture_square : str):
    arm.moveToSquare(capture_square)
    arm.pickupPiece()
    deltax = arm.Arm_constants.SQUARE_LOCATIONS[3][4][0] - arm.Arm_constants.SQUARE_LOCATIONS[3][3][0]
    deltay = arm.Arm_constants.SQUARE_LOCATIONS[3][4][1] - arm.Arm_constants.SQUARE_LOCATIONS[3][3][1]

    trashx = arm.Arm_constants.SQUARE_LOCATIONS[3][0][0] - (3 * deltax)
    trashy = arm.Arm_constants.SQUARE_LOCATIONS[3][0][1] - (3 * deltay)

    arm.Arm_constants.ARM.set_position(trashx, trashy, arm.Arm_constants.POS_Z_HIGHEST_PIECE, 180, 0, 0, None, 100, 50, wait=True)

    arm.Arm_constants.ARM.open_lite6_gripper()
    arm.time.sleep(1)
    arm.Arm_constants.ARM.stop_lite6_gripper()
    