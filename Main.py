import pygame
import Board
from BoardPainter import *
from BigCell import *

print("")
player_number = int(input("Please enter how many players will be playing(2-4): "))
print("")
create_player_order(player_number)

pygame.init()
screen = pygame.display.set_mode((800, 800))
font = pygame.font.Font(None, 40)
done = False
first_move = True

board = Board.Board(6, 5)
painter = BoardPainter(120, 40, screen, font)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            cell, direction = painter.find_position(mouse_x, mouse_y, board)
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


    screen.fill(pygame.Color("black"))
    painter.draw_board(board)
    pygame.display.flip()
