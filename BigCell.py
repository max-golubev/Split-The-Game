from enum import Enum
import random

NOONE = -1
PLAYER_1 = 1
PLAYER_2 = 2
PLAYER_3 = 3
PLAYER_4 = 4

PLAYERS = [PLAYER_1, PLAYER_2, PLAYER_3, PLAYER_4]
PLAYER_ORDER = []


def create_player_order(player_number):
    for i in range(player_number):
        PLAYER_ORDER.append(PLAYERS[i])


class Direction(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4
    OUTSIDE = 5

    def get_opposite(self):
        if self == Direction.TOP:
            return Direction.BOTTOM
        if self == Direction.RIGHT:
            return Direction.LEFT
        if self == Direction.BOTTOM:
            return Direction.TOP
        if self == Direction.LEFT:
            return Direction.RIGHT
        return Direction.OUTSIDE


class BigCell:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.max_x = width - 1
        self.max_y = height - 1

        self.small_cells = {
            Direction.TOP : NOONE,
            Direction.RIGHT : NOONE,
            Direction.BOTTOM : NOONE,
            Direction.LEFT : NOONE,
        }

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_big_cell_owner(self):
        for next in Direction:
            if next == Direction.OUTSIDE:
                continue
            cell_owner = self.get_small_cell_owner(next)
            if cell_owner != NOONE:
                return cell_owner
        return NOONE

    def clear(self):
        for next in Direction:
            if next == Direction.OUTSIDE:
                continue
            self.set_small_cell_owner(next, NOONE)

    def capture(self, player, capturing: Direction, captured_cell):
        empty_directions = []

        for next in Direction:
            if next == Direction.OUTSIDE:
                continue
            elif not self.has_small_cell(next):
                continue
            elif self.get_small_cell_owner(next) != NOONE:
                self.set_small_cell_owner(next, player)
            else:
                empty_directions.append(next)

        if self.get_small_cell_owner(capturing) == NOONE:
            self.set_small_cell_owner(capturing, player)
        else:
            random_index = random.randint(0, len(empty_directions) - 1)
            self.set_small_cell_owner(empty_directions[random_index], player)

    def is_full(self):
        for next in Direction:
            if next == Direction.OUTSIDE:
                continue
            if not self.has_small_cell(next):
                continue
            if self.get_small_cell_owner(next) == NOONE:
                return False
        return True

    def get_small_cell_owner(self, direction):
        return self.small_cells[direction]

    def set_small_cell_owner(self, direction, owner):
        if direction == Direction.OUTSIDE:
            raise ValueError("can't set owner: %d" % owner)
        self.small_cells[direction] = owner

    def has_top(self):
        return self.y != 0

    def has_left(self):
        return self.x != 0

    def has_bottom(self):
        return self.y != self.max_y

    def has_right(self):
        return self.x != self.max_x

    def has_small_cell(self, direction):
        if direction == Direction.TOP:
            return self.has_top()
        if direction == Direction.RIGHT:
            return self.has_right()
        if direction == Direction.BOTTOM:
            return self.has_bottom()
        if direction == Direction.LEFT:
            return self.has_left()
        if direction == Direction.OUTSIDE:
            return False
        raise ValueError("unsupported direction " + repr(direction))
