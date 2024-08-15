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

    def show_highlights(screen, moves, coords):
        if moves != []:
            for move in moves:
                if str(coords[0]) == move[0] and str(coords[1]) == move[1]:
                    rect = pygame.draw.rect(screen, (50, 0, 0), pygame.Rect(int(move[3]) * SQSIZE, int(move[2]) * SQSIZE, SQSIZE, SQSIZE), 10)