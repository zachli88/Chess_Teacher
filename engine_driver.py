import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import chess
import chess.svg
import io
import cairosvg
import queue

def position_to_uci(position):
    row, col = position
    uci_col = chr(ord('a') + col)
    uci_row = str(8 - int(row))
    return uci_col + uci_row

class ChessApp(tk.Tk):
    def __init__(self):
        """
        Initializes UI in tkinter with given title, size
        """
        super().__init__()

        self.title("Chess Engine UI")
        self.geometry("400x400")

        self.board = chess.Board()
        self.create_widgets()

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

    def frame_clicked(self, event):
        square_dim = 360/8
        piece_x = int((event.x - 20) // square_dim)
        piece_y = int((event.y - 20) // square_dim)

        uci = position_to_uci((piece_y, piece_x))
        print("uci", uci)

    def refresh_board(self,):
        # does some fancy chess svg stuff to display self.board
        svg_data = chess.svg.board(self.board)
        png_data = io.BytesIO()
        cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=png_data)
        img_data = Image.open(png_data)
        img_data = img_data.resize((400, 400), Image.LANCZOS)
        img_data = ImageTk.PhotoImage(img_data)

        # gets rid of existing board
        if hasattr(self, 'chessboard_label'):
            self.chessboard_label.destroy()

        # puts picture on UI
        self.chessboard_label = ttk.Label(self.chessboard_frame, image=img_data)
        self.chessboard_label.image = img_data
        self.chessboard_label.bind("<Button-1>", self.frame_clicked)
        self.chessboard_label.pack()

    def next_move(self):
        # gets first possible move, makes it
        if self.board.legal_moves:
            move = self.board.legal_moves.__iter__().__next__()
            self.board.push(move)
            self.refresh_board()

    def previous_move(self):
        # undoes last move
        if len(self.board.move_stack) > 0:
            self.board.pop()
            self.refresh_board()


class Task():
    def __init__(self):
        self.cmd_id = 0
    
    def exec(self):
        pass

class Task():
    def __init__():
        pass

    def execute():
        print("HELLO")

def main():
    tasks = queue.Queue()

    while True:
        task = tasks.get()

        if isinstance(task, Task):
            task.execute()
        else:
            raise("Invalid Task:")
        
if __name__ == "__main__":
    app = ChessApp()
    app.mainloop()
