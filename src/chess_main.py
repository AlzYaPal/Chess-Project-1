import sys, pygame
from chess_engine import *
from vars import *
from colours import *
from graphics import *
from moves import *

class Main:
    def __init__(self):
        pygame.init()
        self.engine = Engine()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = self.engine.get_board()
        self.pieces = {"wR": pygame.transform.scale(pygame.image.load("assets/pieces/wR.png"), (SQSIZE, SQSIZE)),
                  "wN": pygame.transform.scale(pygame.image.load("assets/pieces/wN.png"), (SQSIZE, SQSIZE)),
                  "wB": pygame.transform.scale(pygame.image.load("assets/pieces/wB.png"), (SQSIZE, SQSIZE)),
                  "wQ": pygame.transform.scale(pygame.image.load("assets/pieces/wQ.png"), (SQSIZE, SQSIZE)),
                  "wK": pygame.transform.scale(pygame.image.load("assets/pieces/wK.png"), (SQSIZE, SQSIZE)),
                  "wp": pygame.transform.scale(pygame.image.load("assets/pieces/wp.png"), (SQSIZE, SQSIZE)),
                  "bR": pygame.transform.scale(pygame.image.load("assets/pieces/bR.png"), (SQSIZE, SQSIZE)),
                  "bN": pygame.transform.scale(pygame.image.load("assets/pieces/bN.png"), (SQSIZE, SQSIZE)),
                  "bB": pygame.transform.scale(pygame.image.load("assets/pieces/bB.png"), (SQSIZE, SQSIZE)),
                  "bQ": pygame.transform.scale(pygame.image.load("assets/pieces/bQ.png"), (SQSIZE, SQSIZE)),
                  "bK": pygame.transform.scale(pygame.image.load("assets/pieces/bK.png"), (SQSIZE, SQSIZE)),
                  "bp": pygame.transform.scale(pygame.image.load("assets/pieces/bp.png"), (SQSIZE, SQSIZE)),
                  }
        self.clicks = 0
        self.squares = []
        self.whiteToMove = True

        pygame.display.set_icon(pygame.image.load("assets/icon/icon.png"))
        pygame.display.set_caption("Chess AI")
    
    def checkmate():
        font = pygame.font.Font("dahliaregictik.ttf", 64)
    
    def main_loop(self):
        colour = 0
        screen = self.screen
        board = self.board
        whiteToMove = self.whiteToMove
        squares = self.squares
        engine = self.engine
        moves = Moves(board)
        validMoves, inCheck  = moves.getValidMoves(whiteToMove, board)
        moveMade = False #Flag for when a move is made
        checkmate = False
        stalemate = False
        running = True
        while running:
            screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                        colour += 1
                        if colour == 12:
                            colour = 0
                    elif event.key == pygame.K_z:
                        try:
                            move = engine.moveLog[-1]
                            squares = move[0]
                            piece = move[1]
                            board[int(squares[0])][int(squares[1])] = board[int(squares[2])][int(squares[3])]
                            board[int(squares[2])][int(squares[3])] = piece
                            engine.moveLog.pop(-1)
                            squares = []
                            moveMade = True
                        except IndexError:
                            pass
                    elif event.key == pygame.K_x:
                        self.clicks = 0
                        try:
                            for i in range(2):
                                squares.pop(-1)
                        except IndexError:
                            pass

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    squares.append(pos[1] // SQSIZE)
                    squares.append(pos[0] // SQSIZE)
                    
                    
                    if board[squares[-2]][squares[-1]] != "--" and self.clicks == 0:
                        self.clicks = 1
                    elif self.clicks == 1:
                        self.clicks = 0
                        move = str(squares[0]) + str(squares[1]) + str(squares[2]) + str(squares[3])
                        pieceTaken = board[squares[2]][squares[3]]
                        if move in validMoves:
                            engine.moveLog.append((move, board[squares[2]][squares[3]]))
                            board[squares[2]][squares[3]] = board[squares[0]][squares[1]]
                            board[squares[0]][squares[1]] = "--"
                            squares = []
                            moveMade = True
                        else:
                            clicks = 0
                            squares = []

                    else:
                        for i in range(2):
                            squares.pop(-1)
            if moveMade:
                whiteToMove = not whiteToMove
                validMoves, inCheck = moves.getValidMoves(whiteToMove, board)
                moveMade = False
                if validMoves == []:
                    if inCheck == True:
                        inCheckmate = True
                    else:
                        inStalemate = True
                
            if inCheckmate:
                self.checkmate()
            
            if inStalemate:
                self.stalemate()



            Graphics.draw_squares(screen, colours[colour])
            Graphics.draw_pieces(screen, board, self.pieces)
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
            


main = Main()
main.main_loop()