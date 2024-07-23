from vars import *
import pygame
pygame.init()

class Graphics:

    def draw_squares(surface, colour):
        for row in range(ROWSIZE):
            for col in range(COLSIZE):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(surface, colour, (row * SQSIZE, col * SQSIZE, SQSIZE, SQSIZE))

    def draw_pieces(screen, board, pieces):
        for row in range(ROWSIZE):
            for col in range(COLSIZE):
                if board[row][col] != "--":
                    screen.blit(pieces[board[row][col]], (col * SQSIZE, row * SQSIZE))