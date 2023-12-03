import enum


class Direction(enum.Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4


class BigCell:
    max_x = 2 #TODO
    max_y = 2 #TODO

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.owner = None

        self.small_cels = {}
        if self.y != 0:
            self.small_cels[Direction.TOP] = False
        if self.x != BigCell.max_x:
            self.small_cels[Direction.RIGHT] = False
        if self.y != BigCell.max_y:
            self.small_cels[Direction.BOTTOM] = False
        if self.x != 0:
            self.small_cels[Direction.LEFT] = False

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_owner(self):
        return self.owner

    def set_owner(self, new_owner):
        self.owner = new_owner

    def fill_small_cell(self, direction: Direction):
        self.small_cels[direction] = True

    def clear(self):
        for direction in self.small_cels:
            self.small_cels[direction] = False

    def is_full(self):
        for direction in self.small_cels:
            if not self.small_cels[direction]:
                return False
        return True
