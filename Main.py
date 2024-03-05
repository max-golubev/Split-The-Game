import pygame
import Board
from BoardPainter import *
from BigCell import *

pygame.init()
screen = pygame.display.set_mode(BOARD_SIZE)
font = pygame.font.Font(None, 40)

phase = 1
done = False
first_move = True

columns = 6
rows = 5
board = Board.Board(columns, rows)
board_painter = BoardPainter(columns, rows, screen, font)
initial_screen_painter = InitialScreenPainter(screen, font)

initial_screen_painter.paint_initial_screen()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if phase == 1:
                if is_within(play_button_top_coord, play_button_top_coord + play_button_height,
                                                    play_button_left_coord, play_button_left_coord + play_button_width,
                                                    mouse_x, mouse_y):
                    initial_screen_painter.player_count_screen()
                    phase += 1

            if phase == 2:
                if is_within(count_button_top_coord, count_button_top_coord + count_button_height,
                             button_left_coordinate_2, button_left_coordinate_2 + count_button_width,
                             mouse_x, mouse_y):
                    player_count = 2
                    create_player_order(player_count)
                    phase += 1
                    continue

                elif is_within(count_button_top_coord, count_button_top_coord + count_button_height,
                               button_left_coordinate_3, button_left_coordinate_3 + count_button_width,
                               mouse_x, mouse_y):
                    player_count = 3
                    create_player_order(player_count)
                    phase += 1
                    continue

                elif is_within(count_button_top_coord, count_button_top_coord + count_button_height,
                               button_left_coordinate_4, button_left_coordinate_4 + count_button_width,
                               mouse_x, mouse_y):
                    player_count = 4
                    create_player_order(player_count)
                    phase += 1
                    continue

            if phase == 3:
                cell, direction = board_painter.find_position(mouse_x, mouse_y, board)
                if cell is not None:
                    #print("you clicked [%d, %d]" % (cell.get_x(), cell.get_y()) + ", dir: " + repr(direction))
                    if direction != Direction.OUTSIDE:
                        if board.perform_turn(cell, direction):
                            if not first_move:
                                has_won, winner = board.has_won()
                                #print(board.has_won())
                                if has_won:
                                    print(f"The winner is player number {winner}!")
                                    done = True
                                    break
                            first_move = False
                            board.finish_turn()
    if phase == 1:
        initial_screen_painter.paint_initial_screen()

                            board.finish_turn(PLAYER_ORDER)

            if phase == 4:
                screen.fill(pygame.Color("black"))
                font = pygame.font.Font('freesansbold.ttf', 40)
                text = font.render(f"The winner is player number {alive_players[0]}!", True,
                                   PLAYER_COLORS[alive_players[0]])
                screen.blit(text, (150, 400))

    if phase == 3:
        screen.fill(pygame.Color("black"))
        board_painter.draw_board(board)
    pygame.display.flip()
