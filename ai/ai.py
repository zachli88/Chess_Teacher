import chess
from stockfish import Stockfish

stockfish = Stockfish("/opt/homebrew/Cellar/stockfish/15.1/bin/stockfish")
# stockfish = Stockfish("/usr/local/Cellar/stockfish/15.1/bin/stockfish")
stockfish.set_depth(20)
stockfish.set_skill_level(20)


def getMove(fen):
    stockfish.set_fen_position(fen)
    return stockfish.get_best_move()


def getEval(): 
    eval_sf = stockfish.get_evaluation()
    if eval_sf['type'] == 'cp':
        return eval_sf['value'] / 100
    else:
        return f"mate in {eval_sf['value']}"

def boardPrint():
    print(stockfish.get_board_visual())





