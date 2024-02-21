import Board
from BigCell import *
import pygame

border_color = (0, 0, 255)
cell_color = (100, 100, 100)

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
