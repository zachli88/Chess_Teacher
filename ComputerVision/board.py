# + (white), - (black)
# 0 = empty
# 1 = pawn
# 2 = knight
# 3 = bishop
# 4 = rook
# 5 = queen
# 6 = king
 

def get_mapping(piece_int):
   piece_int = -piece_int
   if piece_int == 0:
       return " "
   elif piece_int == 1:
       return "♙"
   elif piece_int == 2:
       return "♘"
   elif piece_int == 3:
       return "♗"
   elif piece_int == 4:
       return "♖"
   elif piece_int == 5:
       return "♕"
   elif piece_int == 6:
       return "♔"	
   elif piece_int == -1:
       return "♟︎"
   elif piece_int == -2:
       return "♞"
   elif piece_int == -3:
       return "♝"
   elif piece_int == -4:
       return "♜"
   elif piece_int == -5:
       return "♛"
   elif piece_int == -6:
       return "♚"
   elif piece_int == 9:
       return "?"

def get_empty_grid():
    print("Hello")

class Board:
    def __init__(self, empty_board):
        self.board = [ [0]*8 for i in range(8)]
        board = self.board
        board[6][0] = 1
    
    def __str__(self):
        board_str = ""
        for i, row in enumerate(self.board):
            board_str += str(8-i) + " |"
            for cell in row:
                board_str += get_mapping(cell)
                board_str += "|"
            board_str += "\n"
        board_str += "   a b c d e f g h"
        return board_str
    
