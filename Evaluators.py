import chess

def gpt3_eval(board: chess.Board):
    if board.is_stalemate():
        return 0

    if board.is_checkmate():
        if board.turn == chess.BLACK:
            return 10000000000
        else:
            return -10000000000
        
    # Initialize the score
    score = 0

    # Piece values
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0 
    }

    # Evaluate each square on the board
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
        piece_value = piece_values[piece.piece_type]
        
        # Assign positive or negative values based on piece color (positive for white, negative for black)
        if piece.color:
            score += piece_value
        else:
            score -= piece_value
    
    return score

