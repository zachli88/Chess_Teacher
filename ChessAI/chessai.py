import chess

from stockfish import Stockfish
stockfish = Stockfish("/opt/homebrew/Cellar/stockfish/15.1/bin/stockfish")
stockfish.set_depth(20)
stockfish.set_skill_level(20)
def getMove(fen):
    stockfish.set_fen_position(fen)
    return stockfish.get_best_move()
