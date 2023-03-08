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

class ChessBoard:
    def __init__(self):
        self.board = [ [0]*8 for i in range(8)]
        board = self.board

        board[0] = [-4, -2, -3, -5, -6, -3, -2, -4]
        board[1] = [-1] * 8
        board[6] = [1] * 8
        board[7] = [4, 2, 3, 5, 6, 3, 2, 4]


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
    

    def get_fen(self):
        board = self.board
        fen = ''
        for row in board:
            empty = 0
            for square in row:
                if square == 0:
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    if square > 0:
                        fen += 'PNBRQK'[square-1]
                    else:
                        fen += 'pnbrqk'[-square-1]
            if empty > 0:
                fen += str(empty)
            fen += '/'
        fen = fen[:-1]  # remove last '/'
        
        # add the side to move
        fen += ' w '  # assume white to move
        
        # add the castling rights
        castling = ''
        if board[0][4] == 4 and board[0][0] == 6:
            castling += 'K'
        if board[0][4] == 4 and board[0][7] == 6:
            castling += 'Q'
        if board[7][4] == -4 and board[7][0] == -6:
            castling += 'k'
        if board[7][4] == -4 and board[7][7] == -6:
            castling += 'q'
        if castling == '':
            fen += '-'
        else:
            fen += castling
        
        # add the en passant target square
        en_passant = ''
        for i in range(8):
            if board[3][i] == 1 and board[1][i] == -1:
                en_passant = chr(ord('a')+i) + '6'
                break
            if board[4][i] == -1 and board[6][i] == 1:
                en_passant = chr(ord('a')+i) + '3'
                break
        if en_passant == '':
            fen += ' -'
        else:
            fen += ' ' + en_passant
        
        # add the halfmove clock and fullmove number
        fen += ' 0 1'
        
        return fen
        
