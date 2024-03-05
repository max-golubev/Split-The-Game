from BigCell import *


class Board:
    def __init__(self, width, height):
        self.current_player = PLAYER_1
        self.columns = width  # in-game x
        self.rows = height  # in-game y
        self.cells = width * [None]
        for x in range(0, width):
            column = height * [None]
            self.cells[x] = column
            for y in range(0, height):
                column[y] = BigCell(x, y, width, height)

    def get_current_player(self):
        return self.current_player

    def finish_turn(self, player_order):
        self.current_player = self.compute_next_player(player_order)
        return self.get_current_player()

    def perform_turn(self, cell: BigCell, direction: Direction):
        if cell.get_small_cell_owner(direction) == NOONE:
            if cell.get_big_cell_owner() == self.current_player or cell.get_big_cell_owner() == NOONE:
                cell.set_small_cell_owner(direction, self.current_player)
                if cell.is_full():
                    self.explode(cell)
                return True
        return False

    def explode(self, cell: BigCell):
        queue = [cell]
        while len(queue) > 0:
            next = queue.pop(0)
            next.clear()
            for next in self.neighbours(next).items():
                dir, neighbour = next
                origin = dir.get_opposite()
                neighbour.capture(self.current_player, origin, cell)
                if neighbour.is_full():
                    queue.append(neighbour)

    def neighbours(self, cell: BigCell):
        result = {}
        x = cell.get_x()
        y = cell.get_y()
        if cell.has_top():
            result[Direction.TOP] = self.get_big_cell(x, y - 1)
        if cell.has_right():
            result[Direction.RIGHT] = self.get_big_cell(x + 1, y)
        if cell.has_bottom():
            result[Direction.BOTTOM] = self.get_big_cell(x, y + 1)
        if cell.has_left():
            result[Direction.LEFT] = self.get_big_cell(x - 1, y)
        return result

    def compute_next_player(self, player_order):
        current = self.get_current_player()
        if current in player_order:
            index = player_order.index(current)
            if index == (len(player_order) - 1):
                return player_order[0]
            else:
                return player_order[index + 1]
        else:
            raise ValueError("Unknown player: " + repr(current))

    def get_big_cell(self, col, row) -> BigCell:
        return self.cells[col][row]

    def get_columns_number(self):
        return self.columns

    def get_rows_number(self):
        return self.rows

    def alive_players(self):
        alive_players = []
        for x in range(0, self.columns):
            for y in range(0, self.rows):
                contestant = Board.get_big_cell(self, x, y).get_big_cell_owner()
                if contestant == NOONE:
                    continue
                elif contestant not in alive_players:
                    alive_players.append(contestant)
        return alive_players
