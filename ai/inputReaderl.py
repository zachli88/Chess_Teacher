import chess
import chess.pgn as pgn

pgn_file = open("temp.pgn") 
game = pgn.read_game(pgn_file)

while (game != None) :


    input_params = 0
    board = chess.Board()
    for number, move in enumerate(game.mainline_moves()):
        board.push(move)
        input_params+=1
        if input_params == 1000:
            #neuralnet(bullshit)
            input_params -= 1000
    
    fen = board.fen()
    print(fen)
    print(board)
    game = pgn.read_game(pgn_file)