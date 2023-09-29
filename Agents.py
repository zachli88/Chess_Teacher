from chess import Move, Board
import random

class Agent():
    def get_move(self, board_state: Board) -> Move:
        pass

    def log_info(self, board_state: Board):
        pass

class RandomAgent(Agent):
    def get_move(self, board_state: Board) -> Move:
        options = list(board_state.legal_moves)
        return random.choice(options)

    def log_info(self, board_state: Board):
        pass
