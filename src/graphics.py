from vars import *
import pygame
pygame.init()

class Graphics:

    def draw_squares(screen, colour):
        for row in range(ROWSIZE):
            for col in range(COLSIZE):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(screen, colour, (row * SQSIZE, col * SQSIZE, SQSIZE, SQSIZE))

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

    def pawn_promotion_square(screen, r, c, bishop, knight, rook, queen):
        pygame.draw.rect(screen, (255, 255, 255), (r * SQSIZE, c * SQSIZE, SQSIZE, SQSIZE))
        bishop = pygame.transform.scale(bishop, (SQSIZE // 2 - 2, SQSIZE // 2 - 4))
        knight = pygame.transform.scale(knight, (SQSIZE // 2 - 2, SQSIZE // 2 - 4))
        rook = pygame.transform.scale(rook, (SQSIZE // 2 - 2, SQSIZE // 2 - 4))
        queen = pygame.transform.scale(queen, (SQSIZE // 2 - 2, SQSIZE // 2 - 4))
        screen.blit(queen, (SQSIZE * c + 2, SQSIZE * r + 2))
        screen.blit(rook, (SQSIZE * c + 2, SQSIZE * r + (SQSIZE // 2) + 2))
        screen.blit(knight, (SQSIZE * c + (SQSIZE // 2) + 2, SQSIZE * r + 2))
        screen.blit(bishop, (SQSIZE * c + (SQSIZE // 2) + 2, SQSIZE * r + (SQSIZE // 2) + 2))
        pygame.display.flip()