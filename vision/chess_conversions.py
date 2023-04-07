def coord_sum(uci, diffs):
    r, c = uci_to_position(uci)
    return diffs[r][c]


def castle_sums(move, diffs):
    if move == "e8c8":
        return coord_sum("a8", diffs) + coord_sum("d8", diffs)
    elif move == "e1c1":
        return coord_sum("a1", diffs) + coord_sum("d1", diffs)
    elif move == "e8g8":
        return coord_sum("f8", diffs) + coord_sum("h8", diffs)
    elif move == "e1g1":
        return coord_sum("f1", diffs) + coord_sum("h1", diffs)
    return 0


def get_castle_squares(move):
    if move == "e8c8":
        return "a8d8"
    elif move == "e1c1":
        return "a1d1" 
    elif move == "e8g8":
        return "h8f8"
    elif move == "e1g1":
        return "h1f1"


def position_to_uci(position):
    row, col = position
    uci_col = chr(ord('a') + col)
    uci_row = str(8 - row)
    return uci_col + uci_row


def uci_to_position(uci_square):
    file, rank = uci_square[0], int(uci_square[1])
    row = 8 - rank
    col = ord(file) - ord('a')
    return row, col