import pygame
from colours import *
from vars import *
pygame.init()

class Graphics:

    def drawSquares(screen, colour): #Drawing the black and white squares on the board
        for row in range(rowSize):
            for col in range(colSize):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(screen, colour, (row * squareSize, col * squareSize, squareSize, squareSize))

    def drawPieces(screen, board, pieces): #Drawing the pieces on the board
        for row in range(rowSize):
            for col in range(colSize):
                if board[row][col] != "--":
                    screen.blit(pieces[board[row][col]], (col * squareSize, row * squareSize))

    def showHighlights(screen, moves, coords): #Highlighting the squares for valid moves
        if moves != []:
            for move in moves:
                if str(coords[0]) == move[0] and str(coords[1]) == move[1]:
                    rect = pygame.draw.rect(screen, (50, 0, 0), pygame.Rect(int(move[3]) * squareSize, int(move[2]) * squareSize, squareSize, squareSize), 10)

    def pawnPromotionSquare(screen, r, c, bishop, knight, rook, queen, colour):
        if (r + c) % 2 == 0:
            pygame.draw.rect(screen, (255, 255, 255), (c * squareSize, r * squareSize, squareSize, squareSize))
        else:
            pygame.draw.rect(screen, colours[colour], (c * squareSize, r * squareSize, squareSize, squareSize))
        bishop = pygame.transform.scale(bishop, (squareSize // 2 - 2, squareSize // 2 - 4))
        knight = pygame.transform.scale(knight, (squareSize // 2 - 2, squareSize // 2 - 4))
        rook = pygame.transform.scale(rook, (squareSize // 2 - 2, squareSize // 2 - 4))
        queen = pygame.transform.scale(queen, (squareSize // 2 - 2, squareSize // 2 - 4))
        screen.blit(queen, (squareSize * c + 2, squareSize * r + 2))
        screen.blit(rook, (squareSize * c + 2, squareSize * r + (squareSize // 2) + 2))
        screen.blit(knight, (squareSize * c + (squareSize // 2) + 2, squareSize * r + 2))
        screen.blit(bishop, (squareSize * c + (squareSize // 2) + 2, squareSize * r + (squareSize // 2) + 2))
        pygame.display.flip()