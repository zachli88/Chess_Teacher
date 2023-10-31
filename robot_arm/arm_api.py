import arm as arm
import vision.chess_conversions as cc

# Moves piece on starting square to a given ending square
# inputs: starting_square to move from, ending_square to move to
# output: returns true on success, false on failure
def move_piece(starting_square: str, ending_square: str):
    #movePieceAndRotate
    arm.unrotate()
    arm.movePiece(starting_square, ending_square)
    arm.rotate()

def capture_piece(starting_square: str, ending_square: str):
    # capture part of move piece and rotate
    arm.unrotate()
    remove(ending_square)
    arm.movePiece(starting_square, ending_square)
    arm.rotate()

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

def promote (square: str, piece: str):
    arm.unrotate()
    remove(square)
    arm.rotate()
    y = 0
    if (piece == "R"):
        y = 1
    elif (piece == "B"):
        y = 2
    elif (piece == "K"):
        y = 3

    print(arm.Arm_constants.RESERVE_LOCATIONS)    
    arm.Arm_constants.ARM.set_position(arm.Arm_constants.RESERVE_LOCATIONS[y][0][0],
                                    arm.Arm_constants.RESERVE_LOCATIONS[y][0][1],
                                    arm.Arm_constants.POS_Z_HIGHEST_PIECE, 180, 0, 0, None, 100, 50, wait=True) 
    
    arm.Arm_constants.ARM.open_lite6_gripper()
    arm.time.sleep(1)
    arm.Arm_constants.ARM.stop_lite6_gripper()

#pickup_piece()
    curPos = arm.Arm_constants.ARM.position
    arm.Arm_constants.ARM.set_position(curPos[0], curPos[1], arm.Arm_constants.POS_Z_BOARD, 180, 0, 0, None, 100, 50, wait=True)

    arm.Arm_constants.ARM.close_lite6_gripper()
    arm.time.sleep(1)
    arm.Arm_constants.ARM.stop_lite6_gripper()

    arm.Arm_constants.ARM.set_position(curPos[0], curPos[1], arm.Arm_constants.POS_Z_HIGHEST_PIECE, 180, 0, 0, None, 100, 50, wait=True)

#move piece
    indices = arm.squareToIndices(square)
    arm.Arm_constants.ARM.set_position(arm.Arm_constants.SQUARE_LOCATIONS[indices[0]][indices[1]][0],
                                    arm.Arm_constants.SQUARE_LOCATIONS[indices[0]][indices[1]][1],
                                      arm.Arm_constants.POS_Z_HIGHEST_PIECE, 180, 0, 0, None, 100, 50, wait=True) 

#drop_piece()
    curPos = arm.Arm_constants.ARM.position
    arm.Arm_constants.ARM.set_position(curPos[0], curPos[1], arm.Arm_constants.POS_Z_BOARD, 180, 0, 0, None, 100, 50, wait=True)

    arm.Arm_constants.ARM.open_lite6_gripper()
    arm.time.sleep(1)
    arm.Arm_constants.ARM.stop_lite6_gripper()

    arm.Arm_constants.ARM.set_position(curPos[0], curPos[1], arm.Arm_constants.POS_Z_HIGHEST_PIECE, 180, 0, 0, None, 100, 50, wait=True)