import Board
from BigCell import *
import pygame

board_height = 900
board_width = 900
BOARD_SIZE = (board_height, board_width)

cell_border_color = (0, 0, 255)
cell_color = (100, 100, 100)

PLAYER_COLORS = {}
PLAYER_COLORS[PLAYER_1] = (255, 0, 0)
PLAYER_COLORS[PLAYER_2] = (0, 255, 0)
PLAYER_COLORS[PLAYER_3] = (0, 0, 255)
PLAYER_COLORS[PLAYER_4] = (255, 255, 0)
PLAYER_COLORS[NOONE] = cell_color

# player count buttons
count_button_height = 90
count_button_width = count_button_height
count_button_top_coord = 450
button_left_coordinate_2 = board_width / 2 - count_button_height * 2 - count_button_height
button_left_coordinate_3 = board_width / 2 - count_button_height / 2
button_left_coordinate_4 = board_width / 2 + count_button_height * 2

# Initial screen buttons
play_button_height = 90
play_button_width = 180
play_button_top_coord = 300
play_button_left_coord = (board_width / 2) - (play_button_width / 2)

initial_screen_colors = {"title_color": (2, 205, 212),
                         "background": (0, 0, 0),
                         "buttons_color": (194, 194, 194),
                         "button_border": (37, 20, 224),
                         "button_text_color": (255, 0, 0)}


class BoardPainter:
    def __init__(self, rows_number, columns_number, screen: pygame.Surface, font: pygame.font.Font):
        self.screen = screen
        self.font = font
        self.x0 = 10
        self.y0 = self.x0

        higher_side_count = 0
        lower_board_length = 0
        if rows_number >= columns_number:
            higher_side_count = rows_number
        else:
            higher_side_count = columns_number
        if (board_height - 40) <= board_width:
            lower_board_length = board_height - 40
        else:
            lower_board_length = board_width

        self.big_cell_height = (lower_board_length - self.x0 * 2) // higher_side_count  # size in pixels
        self.small_cell_height = self.big_cell_height // 3  # size in pixels

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
            pygame.draw.line(self.screen, cell_border_color, (xx, top), (xx, bottom))

        for row in range(0, rows + 1):
            yy = self.y0 + self.big_cell_height * row
            pygame.draw.line(self.screen, cell_border_color, (self.x0, yy), (self.x0 + width, yy))

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


class InitialScreenPainter:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def paint_initial_screen(self):
        InitialScreenPainter.paint_title(self)

        # play button
        pygame.draw.rect(self.screen, initial_screen_colors["buttons_color"],
                         (play_button_left_coord, play_button_top_coord, play_button_width, play_button_height))
        InitialScreenPainter.draw_rect_borders(self, play_button_top_coord, play_button_left_coord,
                                               play_button_height, play_button_width,
                                               initial_screen_colors["button_border"], 2)

        play_text_size = 40
        font = pygame.font.Font('freesansbold.ttf', play_text_size)
        play_text = font.render('Play', True, initial_screen_colors["button_text_color"])
        self.screen.blit(play_text, (board_width / 2 - play_text_size,
                                     play_button_top_coord + (play_button_height - play_text_size) / 2))

    def player_count_screen(self):
        InitialScreenPainter.paint_title(self)
        font = pygame.font.Font('freesansbold.ttf', 40)
        prompt_text = font.render('Choose number of player:', True, initial_screen_colors["button_text_color"])
        self.screen.blit(prompt_text, (200, 300))

        button_text_size = 50

        # button for 2 players
        pygame.draw.rect(self.screen, initial_screen_colors["buttons_color"],
                         (button_left_coordinate_2, count_button_top_coord, count_button_height, count_button_height))
        InitialScreenPainter.draw_rect_borders(self, count_button_top_coord, button_left_coordinate_2,
                                               count_button_height, count_button_height,
                                               initial_screen_colors["button_border"], 2)
        font = pygame.font.Font('freesansbold.ttf', button_text_size)
        text = font.render('2', True, initial_screen_colors["button_text_color"])
        self.screen.blit(text, (button_left_coordinate_2 + 32,
                                count_button_top_coord + (count_button_height - button_text_size) / 2 + 3))

        # button for 3 players
        pygame.draw.rect(self.screen, initial_screen_colors["buttons_color"],
                         (button_left_coordinate_3, count_button_top_coord, count_button_height, count_button_height))
        InitialScreenPainter.draw_rect_borders(self, count_button_top_coord, button_left_coordinate_3,
                                               count_button_height, count_button_height,
                                               initial_screen_colors["button_border"], 2)
        font = pygame.font.Font('freesansbold.ttf', button_text_size)
        text = font.render('3', True, initial_screen_colors["button_text_color"])
        self.screen.blit(text, (button_left_coordinate_3 + 32,
                                count_button_top_coord + (count_button_height - button_text_size) / 2 + 3))

        # button for 4 players
        pygame.draw.rect(self.screen, initial_screen_colors["buttons_color"],
                         (button_left_coordinate_4, count_button_top_coord, count_button_height, count_button_height))
        InitialScreenPainter.draw_rect_borders(self, count_button_top_coord, button_left_coordinate_4,
                                               count_button_height, count_button_height,
                                               initial_screen_colors["button_border"], 2)
        font = pygame.font.Font('freesansbold.ttf', button_text_size)
        text = font.render('4', True, initial_screen_colors["button_text_color"])
        self.screen.blit(text, (button_left_coordinate_4 + 30,
                                count_button_top_coord + (count_button_height - button_text_size) / 2  + 3))

    def draw_rect_borders(self, top_y_coordinate, left_x_coordinate, rect_height, rect_width, color, line_width=1):
        # top border
        pygame.draw.line(self.screen, color, (left_x_coordinate - 1, top_y_coordinate - 1),
                         (left_x_coordinate + rect_width + 1, top_y_coordinate - 1), line_width + 1)
        # left border
        pygame.draw.line(self.screen, color, (left_x_coordinate - 1, top_y_coordinate - 1),
                         (left_x_coordinate - 1, top_y_coordinate + rect_height + 1), line_width + 1)
        # bottom border
        pygame.draw.line(self.screen, color, (left_x_coordinate - 1, top_y_coordinate + rect_height + 1),
                         (left_x_coordinate + rect_width + 1, top_y_coordinate + rect_height + 1), line_width)
        # right border
        pygame.draw.line(self.screen, color, (left_x_coordinate + rect_width + 1, top_y_coordinate - 1),
                         (left_x_coordinate + rect_width + 1, top_y_coordinate + rect_height + 1), line_width)

    def paint_title(self):
        self.screen.fill(initial_screen_colors["background"])
        font = pygame.font.Font('freesansbold.ttf', 80)
        title_text = font.render('The Split', True, initial_screen_colors["title_color"])
        self.screen.blit(title_text, (260, 100))


def is_within(top_y_coordinate, bottom_y_coordinate, left_x_coordinate, right_x_coordinate, x, y):
    if left_x_coordinate < x < right_x_coordinate:
        if top_y_coordinate < y < bottom_y_coordinate:
            return True
    return False
