import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from xarm.wrapper import XArmAPI


#  * pickup_piece( str -> name of the square) -> pick up a piece from the board
#  * place_piece( str -> name of the square) -> place a piece on the board
#  * move_piece( str -> name of the square, str -> name of the square) -> move a piece from one square to another
#  * constants: size of the board, size of the squares, size of highest piece
#  * (0, [87.0, -0.0, 154.199997, 180.00002, 0.0, -0.0])
#  * tuple when the arm is just touching the board [x, y, z, roll, pitch, yaw]
#  * (0, [163.208542, 0.025312, 135.205475, -179.992629, -3.380279, 0.091444])

#  * positive z values make the arm go up

class Arm_constants:
    SIZE_SQUARE : int = 0
    SIZE_BOARD : int = 0
    POS_Z_BOARD : int = 0
    POS_Z_HIGHEST_PIECE : int = 0
    OFFSET_X : int = 0
    OFFSET_Y : int = 0
    POS_Z_BASE_BOARD : int = 135

    # def __init__(self, size_square, size_board, pos_z_board, pos_z_highest_piece, offset_x, offset_y):
    #     self.SIZE_SQUARE = size_square
    #     self.SIZE_BOARD = size_board
    #     self.POS_Z_BOARD = pos_z_board
    #     self.POS_Z_HIGHEST_PIECE = pos_z_highest_piece
    #     self.OFFSET_X = offset_x
    #     self.OFFSET_Y = offset_y

def pickup_piece ( grid_square : str): 
    pos = get_grid_position(grid_square)
    arm.set_position(pos[0], pos[1], pos[2] + 50, wait=True)

def place_piece ( grid_square : str): 
    pos = get_grid_position(grid_square)
    arm.set_position(pos[0], pos[1], pos[2] + 50, wait=True)

def move_piece ( grid_square1 : str, grid_square2 : str): 
    pos1 = get_grid_position(grid_square1)
    pos2 = get_grid_position(grid_square2)
    arm.set_position(pos1[0], pos1[1], pos1[2] + 50, wait=True)
    arm.set_position(pos2[0], pos2[1], pos2[2] + 50, wait=True)

def get_grid_position ( grid_square : str):
    pos = (0,0,0)
    # code to get the tuple for the position of the grid given a string representing the square
    return pos

def calibrate():
    # code to calibrate the arm
    # enter a known position for the arm to move relative to the board
    arm.set_position(0, 0, 0, wait=True)


if __name__ == "__main__":
    
# Create an instance of the xArmAPI object
    arm = XArmAPI('192.168.1.166')
    arm.motion_enable(enable=True)
    arm.set_mode(0)
    # Connect to the robot
    arm.connect()

    current_pos = arm.get_position()[1]
    print(current_pos)
    arm.set_position(current_pos[0], current_pos[1], Arm_constants.POS_Z_BASE_BOARD, wait=True)
    #print(current_pos)
    # Move the arm to the target position
    # arm.move_to(x, y, z)
    #arm.reset(wait=True)
    # Disconnect from the robot
    arm.disconnect()