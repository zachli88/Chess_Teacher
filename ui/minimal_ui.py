import tkinter as tk
from tkinter import ttk
import chess
import io
import queue
import cairosvg
from PIL import Image, ImageTk

def position_to_uci(position):
    row, col = position
    uci_col = chr(ord('a') + col)
    uci_row = str(8 - int(row))
    return uci_col + uci_row

def uci_to_position(uci):
    uci_col, uci_row = uci[0], uci[1]
    col = ord(uci_col) - ord('a')
    row = 8 - int(uci_row)
    return row, col


def add_move_dot(svg_data, uci):
        position = uci_to_position(uci)
        square_size = 45  # as 480px board has 60px per square (480/8)
        x = position[1] * square_size + 15
        y = position[0] * square_size + 15

        cx = x + square_size / 2
        cy = y + square_size / 2
        radius = square_size / 8

        svg_circle = f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="#990000" opacity="0.5" />'
        svg_data = svg_data.replace("</svg>", f"{svg_circle}</svg>")        
        return svg_data


def add_square_outline(svg_data, uci):
    position = uci_to_position(uci)
    square_size = 45  # as 480px board has 60px per square (480/8)
    x = position[1] * square_size + 15
    y = position[0] * square_size + 15

    svg_rectangle = f'<rect x="{x}" y="{y}" width="{square_size}" height="{square_size}" stroke="blue" fill="none" stroke-width="2" />'
        
    # Add the rectangle before the last closing tag
    # svg_data = chess.svg.board(self.board)
    svg_data = svg_data.replace("</svg>", f"{svg_rectangle}</svg>")
    return svg_data

def moves_from_square(board, square):
    moves_from_square = board.legal_moves
    moves_from_square = [move for move in moves_from_square if move.from_square == square]
    return moves_from_square

class ChessUI(tk.Tk):
    def __init__(self, using_ui_agent=False):
        """
        Initializes UI in tkinter with given title, size
        """
        super().__init__()

        self.title("Chess Engine UI")
        self.geometry("400x400")

        self.board = chess.Board()
        self.using_ui_agent = using_ui_agent
        self.user_requests = queue.Queue()
        self.user_select = None
        self.create_widgets()
    

    def clear_user_request(self):
        # self.user_requests.queue.clear()
        self.user_select = None
        self.refresh_board()



    def get_user_request(self):
        req = self.user_requests.get()
        self.clear_user_request()
        return req


    def create_widgets(self):
        """
        Creates the widgets in the UI's frame
        """
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Area for chessboard visualization
        self.chessboard_frame = ttk.Frame(self.main_frame, padding=(0, 0, 20, 0))
        self.chessboard_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.refresh_board()


    def board_click(self, event):
        square_dim = 360/8
        piece_x = int((event.x - 20) // square_dim)
        piece_y = int((event.y - 20) // square_dim)

        uci = position_to_uci((piece_y, piece_x))        
        print("uci clicked:", uci)

        if piece_y < 0 or piece_x < 0 or piece_y >= 8 or piece_x >= 8 or len(uci) != 2:
            self.clear_user_request()
            print("oob")
            return

        square = chess.SQUARES[chess.parse_square(uci)]
        piece_at_square = self.board.piece_at(square)

        # moves_from_square = self.board.legal_moves
        # moves_from_square = [move for move in moves_from_square if move.from_square == square]
        moves_from_click = moves_from_square(self.board, square)
        moves_to_click = moves_from_square(self.board, self.user_select)
        print(moves_to_click)
        if piece_at_square and piece_at_square.color == self.board.turn:
            # click on piece of current player's turn

            svg_data = chess.svg.board(self.board)
            svg_data = add_square_outline(svg_data, uci)

            # get legal moves for piece
            for move in moves_from_click:
                svg_data = add_move_dot(svg_data,chess.square_name(move.to_square))
            if len(moves_from_click) > 0:
                self.user_select = square

            self.refresh_board(svg_data)
        elif self.user_select != None and square in [move.to_square for move in moves_to_click ]: 
            requested_move = chess.Move(self.user_select, square)
            print(requested_move)
            # check for promotion in moves to click
            for move in moves_to_click:
                if move.to_square == square and move.promotion:
                    requested_move.promotion = move.promotion
                    break

            self.clear_user_request()
            self.user_requests.put(requested_move)
        else:
            self.clear_user_request()

    def update_board(self, board_data):
        self.board = board_data
        self.refresh_board()

    def refresh_board(self, custom_svg_data=None):
        # does some fancy chess svg stuff to display self.board
        svg_data = chess.svg.board(self.board) if custom_svg_data is None else custom_svg_data
        png_data = io.BytesIO()
        cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=png_data)
        img_data = Image.open(png_data)
        img_data = img_data.resize((400, 400), Image.LANCZOS)
        img_data = ImageTk.PhotoImage(img_data)

        if not hasattr(self, 'chessboard_label'):
            # if label doesn't exist, create it
            self.chessboard_label = ttk.Label(self.chessboard_frame, image=img_data)
            self.chessboard_label.image = img_data
            self.chessboard_label.bind("<Button-1>", self.board_click)
            self.chessboard_label.pack()
        else:
            # if label already exists, just update its image
            self.chessboard_label.configure(image=img_data)
            self.chessboard_label.image = img_data

    def previous_move(self):
        # undoes last move
        if len(self.board.move_stack) > 0:
            self.board.pop()
            self.refresh_board()