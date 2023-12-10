import BigCell


class Board:
    columns = 8
    rows = 8

    def __init__(self):
        board = []
        for x in range(Board.columns + 1):
            for y in range(Board.rows + 1):
                new_cell = BigCell.BigCell(x, y)
                board.append(new_cell)
