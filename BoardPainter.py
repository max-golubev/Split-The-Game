import Board
from BigCell import *
import pygame

board_height = 800
board_width = 800
board_size = (board_height, board_width)

button_height = 80

border_color = (0, 0, 255)
cell_color = (100, 100, 100)

initial_screen_colors = {"title_color": (255, 0, 0),
                         "background": (80, 80, 80),
                         "buttons_color": (194, 194, 194),
                         "button_border": (37, 20, 224)}

PLAYER_COLORS = {}
PLAYER_COLORS[PLAYER_1] = (255, 0, 0)
PLAYER_COLORS[PLAYER_2] = (0, 255, 0)
PLAYER_COLORS[PLAYER_3] = (0, 0, 255)
PLAYER_COLORS[PLAYER_4] = (255, 255, 0)
PLAYER_COLORS[NOONE] = cell_color


class BoardPainter:
    def __init__(self, big_cell_height_in_pixels, small_cell_height_in_pixels, screen: pygame.Surface,
                 font: pygame.font.Font):
        self.big_cell_height = big_cell_height_in_pixels  # size in pixels
        self.small_cell_height = small_cell_height_in_pixels  # size in pixels
        self.screen = screen
        self.font = font
        self.x0, self.y0 = 10, 10

    def draw_board(self, board: Board.Board):
        self.draw_cells(board)
        self.draw_borders(board)
        self.draw_current_player(board)

    def draw_cells(self, board: Board.Board):
        for row in range(0, board.get_rows_number()):
            for col in range(0, board.get_columns_number()):
                cell = board.get_big_cell(col, row)
                self.draw_cell(cell, col, row)

    def draw_cell(self, cell: BigCell, col, row):
        for dir in Direction:
            if cell.has_small_cell(dir):
                square = self.get_small_square_parameters(cell, dir)
                color = self.get_color(cell, dir)
                pygame.draw.rect(self.screen, color, square)

    def draw_borders(self, board: Board.Board):
        columns = board.get_columns_number()
        rows = board.get_rows_number()

        width = columns * self.big_cell_height
        height = rows * self.big_cell_height

        for col in range(0, columns + 1):
            top = self.y0
            bottom = self.y0 + height
            xx = self.x0 + self.big_cell_height * col
            pygame.draw.line(self.screen, border_color, (xx, top), (xx, bottom))

        for row in range(0, rows + 1):
            yy = self.y0 + self.big_cell_height * row
            pygame.draw.line(self.screen, border_color, (self.x0, yy), (self.x0 + width, yy))

    def draw_current_player(self, board: Board.Board):
        player = board.get_current_player()
        text = self.font.render("current player: %d" % player, True, self.get_player_color(player))
        bottom = self.y0 + self.big_cell_height * board.get_rows_number()
        centre = self.x0 + self.big_cell_height * board.get_columns_number() // 2
        self.screen.blit(text, (centre - text.get_width() // 2, bottom + 10))


    def get_color(self, cell: BigCell, dir: Direction):
        owner = cell.get_small_cell_owner(dir)
        return self.get_player_color(owner)

    def get_player_color(self, player):
        return PLAYER_COLORS[player]

    def get_small_square_parameters(self, cell: BigCell, direction: Direction):
        top = self.big_cell_height * cell.get_y() + self.y0
        left = self.big_cell_height * cell.get_x() + self.x0
        delta = (self.big_cell_height - self.small_cell_height) / 2
        if direction == Direction.TOP:
            return (left + delta, top, self.small_cell_height, self.small_cell_height)
        if direction == Direction.RIGHT:
            return (left + self.big_cell_height - self.small_cell_height, top + delta,
                    self.small_cell_height, self.small_cell_height)
        if direction == Direction.BOTTOM:
            return (left + delta, top + self.big_cell_height - self.small_cell_height,
                    self.small_cell_height, self.small_cell_height)
        if direction == Direction.LEFT:
            return (left, top + delta, self.small_cell_height, self.small_cell_height)
        return None

    def find_position(self, mouse_x, mouse_y, board: Board.Board):
        column = (mouse_x - self.x0) // self.big_cell_height
        row = (mouse_y - self.y0) // self.big_cell_height
        if column >= board.get_columns_number() or row >= board.get_rows_number():
            return None, Direction.OUTSIDE

        cell = board.get_big_cell(column, row)

        for dir in Direction:
            if not cell.has_small_cell(dir):
                continue
            square = pygame.Rect(self.get_small_square_parameters(cell, dir))
            if square.collidepoint(mouse_x, mouse_y):
                return cell, dir
        return cell, Direction.OUTSIDE

    def paint_initial_screen(self):
        button_top_coordinate = 500
        self.screen.fill(initial_screen_colors["background"])
        font = pygame.font.Font('freesansbold.ttf', 60)
        text = font.render('The Split', True, initial_screen_colors["title_color"])
        self.screen.blit(text, (260, 100))
        # button for 2 players
        button_left_coordinate_2 = board_width / 2 - button_height * 2 - button_height
        
        pygame.draw.rect(self.screen, initial_screen_colors["buttons_color"],
                         (button_left_coordinate_2, button_top_coordinate, button_height, button_height))
        BoardPainter.draw_rect_borders(self, button_top_coordinate, button_left_coordinate_2,
                                       button_height, button_height, initial_screen_colors["button_border"], 2)

        # button for 3 players
        button_left_coordinate_3 = board_width / 2 - button_height / 2

        pygame.draw.rect(self.screen, initial_screen_colors["buttons_color"],
                         (button_left_coordinate_3, button_top_coordinate, button_height, button_height))
        BoardPainter.draw_rect_borders(self, button_top_coordinate, button_left_coordinate_3,
                                       button_height, button_height, initial_screen_colors["button_border"], 2)

        # button for 4 players
        button_left_coordinate_4 = board_width / 2 + button_height * 2

        pygame.draw.rect(self.screen, initial_screen_colors["buttons_color"],
                         (button_left_coordinate_4, button_top_coordinate, button_height, button_height))
        BoardPainter.draw_rect_borders(self, button_top_coordinate, button_left_coordinate_4,
                                       button_height, button_height, initial_screen_colors["button_border"], 2)

    def draw_rect_borders(self, top_y_coordinate, left_x_coordinate, rect_height, rect_width, color, line_width=1):
        # top border
        pygame.draw.line(self.screen, color, (left_x_coordinate - 1, top_y_coordinate - 1),
                         (left_x_coordinate + rect_width + 1, top_y_coordinate - 1), line_width)
        # right border
        pygame.draw.line(self.screen, color, (left_x_coordinate - 1, top_y_coordinate - 1),
                         (left_x_coordinate - 1, top_y_coordinate + rect_height + 1), line_width)
        # bottom border
        pygame.draw.line(self.screen, color, (left_x_coordinate - 1, top_y_coordinate + rect_height + 1),
                         (left_x_coordinate + rect_width + 1, top_y_coordinate + rect_height + 1), line_width)
        # left border
        pygame.draw.line(self.screen, color, (left_x_coordinate + rect_width + 1, top_y_coordinate - 1),
                         (left_x_coordinate + rect_width + 1, top_y_coordinate + rect_height + 1), line_width)
