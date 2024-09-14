import sys, pygame
from chess_engine import *
from colours import *
from graphics import *
from moves import *
from notation import *
from vars import *

'''
General Algorithm for the Project
'''

class Main:
    def __init__(self):
        pygame.init()
        self.engine = Engine()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = self.engine.get_board()

        # Dictionary to load the names and images (pgn) for all pieces
        self.pieces = {"wR": pygame.transform.scale(pygame.image.load("assets/pieces/wR.png"), (SQSIZE, SQSIZE)), #White Rook
                  "wN": pygame.transform.scale(pygame.image.load("assets/pieces/wN.png"), (SQSIZE, SQSIZE)), #White Knight
                  "wB": pygame.transform.scale(pygame.image.load("assets/pieces/wB.png"), (SQSIZE, SQSIZE)), #White Bishop
                  "wQ": pygame.transform.scale(pygame.image.load("assets/pieces/wQ.png"), (SQSIZE, SQSIZE)), #White Queen
                  "wK": pygame.transform.scale(pygame.image.load("assets/pieces/wK.png"), (SQSIZE, SQSIZE)), #White King
                  "wp": pygame.transform.scale(pygame.image.load("assets/pieces/wp.png"), (SQSIZE, SQSIZE)), #WHite Pawn
                  "bR": pygame.transform.scale(pygame.image.load("assets/pieces/bR.png"), (SQSIZE, SQSIZE)), #Black Rook
                  "bN": pygame.transform.scale(pygame.image.load("assets/pieces/bN.png"), (SQSIZE, SQSIZE)), #Black Knight
                  "bB": pygame.transform.scale(pygame.image.load("assets/pieces/bB.png"), (SQSIZE, SQSIZE)), #Black Bishop
                  "bQ": pygame.transform.scale(pygame.image.load("assets/pieces/bQ.png"), (SQSIZE, SQSIZE)), #Black Queen
                  "bK": pygame.transform.scale(pygame.image.load("assets/pieces/bK.png"), (SQSIZE, SQSIZE)), #Black King
                  "bp": pygame.transform.scale(pygame.image.load("assets/pieces/bp.png"), (SQSIZE, SQSIZE)), #Black Pawn
                  }
        self.clicks = 0
        self.squares = []
        self.whiteToMove = True

        # Added Icon and Caption
        pygame.display.set_icon(pygame.image.load("assets/icon/icon.png"))
        pygame.display.set_caption("Chess AI")
    
    #Checkmate Algorithm
    def checkmate(self, whiteToMove):
        font = pygame.font.Font("assets/font/dahliaregictik.ttf", 44)
        if whiteToMove:
            checkmateStr = font.render("White Wins By Checkmate!", True, (0, 0, 0))
            self.screen.blit(checkmateStr, (10, 268))
        else:
            checkmateStr = font.render("Black Wins By Checkmate!", True, (0, 0, 0))
            self.screen.blit(checkmateStr, (12, 268))

            
    #Stalemate (No Legal Moves + Not In check)
    def stalemate(self):
        font = pygame.font.Font("assets/font/dahliaregictik.ttf", 44)
        stalemateStr = font.render("Draw By Stalemate!", True, (0, 0, 0))
        self.screen.blit(stalemateStr, (10, 268))
        running = True
        while running:
            for e in pygame.event.get():
                if e == pygame.QUIT:
                    running = False
        pygame.quit()
        sys.exit()

    
    def main_loop(self):
        previousMove = ''
        previousPiece = ''
        promotion = False
        promotionTurn = False
        colour = 0
        screen = self.screen
        board = self.board
        whiteToMove = self.whiteToMove
        squares = self.squares
        engine = self.engine
        moves = Moves(board)
        validMoves, inCheck  = moves.getValidMoves(whiteToMove, board, previousMove, previousPiece)
        moveMade = False #Flag for when a move is made
        inCheckmate = False
        inStalemate = False
        notation = Notation()
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
                    
                    if promotion:
                        if ((0 <= pos[1] <= 75 and whiteToMove) or (525 <= pos[1] <= 600 and not whiteToMove)) and \
                            (squares[3] * SQSIZE) <= pos[0] < ((squares[3] + 1) * SQSIZE):
                            if whiteToMove:
                                if pos[1] <= 37.5 and pos[0] - (squares[3] * SQSIZE) <= 37.5:
                                    board[squares[2]][squares[3]] = 'wQ'
                                    board[squares[0]][squares[1]] = '--'
                                elif pos[1] <= 37.5 and 37.5 <= pos[0] - (squares[3] * SQSIZE) < 75:
                                    board[squares[2]][squares[3]] = 'wN'
                                    board[squares[0]][squares[1]] = '--'
                                elif 37.5 <= pos[1] - (squares[2] * SQSIZE) < 75 and pos[0] - (squares[3] * SQSIZE) <= 37.5:
                                    board[squares[2]][squares[3]] = 'wR'
                                    board[squares[0]][squares[1]] = '--'
                                else:
                                    board[squares[2]][squares[3]] = 'wB'
                                    board[squares[0]][squares[1]] = '--'
                            else:
                                if pos[1] >= 562.5 and pos[0] - (squares[3] * SQSIZE) <= 37.5:
                                    board[squares[2]][squares[3]] = 'bB'
                                    board[squares[0]][squares[1]] = '--'
                                elif pos[1] <= 562.5 and 37.5 <= pos[0] - (squares[3] * SQSIZE) < 75:
                                    board[squares[2]][squares[3]] = 'bR'
                                    board[squares[0]][squares[1]] = '--'
                                elif 562.5 <= pos[1] - (squares[2] * SQSIZE) < 525 and pos[0] - (squares[3] * SQSIZE) <= 37.5:
                                    board[squares[2]][squares[3]] = 'bN'
                                    board[squares[0]][squares[1]] = '--'
                                else:
                                    board[squares[2]][squares[3]] = 'bQ'
                                    board[squares[0]][squares[1]] = '--'
                            moveMade = True
                            engine.RFMoveLog[-1] = engine.RFMoveLog[-1] + "=" + board[squares[2]][squares[3]][1]
                            

                    
                    if board[squares[-2]][squares[-1]] != "--" and self.clicks == 0 and not promotion:
                        self.clicks = 1
                        allyColour = 'w' if whiteToMove else 'b'
                    elif self.clicks == 1 and board[pos[1] // SQSIZE][pos[0] // SQSIZE][0] != allyColour:
                        self.clicks = 0
                        move = str(squares[0]) + str(squares[1]) + str(squares[2]) + str(squares[3])
                        pieceTaken = board[squares[2]][squares[3]]
                        if move in validMoves:
                            engine.moveLog.append((move, board[squares[2]][squares[3]]))
                            previousMove = engine.moveLog[-1]
                            engine.RFMoveLog = (notation.toRankFile(engine.moveLog, board, inCheck, inCheckmate))
                            previousPiece = board[squares[0]][squares[1]][1]
                            if move == '0402':
                                board[0][4] = '--'
                                board[0][0] = '--'
                                board[0][2] = 'bK'
                                board[0][3] = 'bR'
                                moves.bKingHasMoved = True
                                moves.bRook1HasMoved = True
                            elif move == '0406':
                                board[0][4] = '--'
                                board[0][7] = '--'
                                board[0][6] = 'bK'
                                board[0][5] = 'bR'
                            elif move == '7472':
                                board[7][4] = '--'
                                board[7][0] = '--'
                                board[7][2] = 'wK'
                                board[7][3] = 'wR'
                            elif move == '7476':
                                board[7][4] = '--'
                                board[7][7] = '--'
                                board[7][6] = 'wK'
                                board[7][5] = 'wR'
                                moves.bKingHasMoved = True
                                moves.bRook1HasMoved = True
                            elif board[int(move[0])][int(move[1])][1] == 'p' and move[1] != move[3] and board[int(move[2])][int(move[3])] == '--':
                                board[squares[2]][squares[3]] = board[squares[0]][squares[1]]
                                board[squares[0]][squares[1]] = '--'
                                if whiteToMove:
                                    board[squares[2] + 1][squares[3]] = '--'
                                else:
                                    board[squares[2] - 1][squares[3]] = '--'

                            elif board[squares[0]][squares[1]][1] == 'p' and ((whiteToMove and squares[2] == 0) or (not whiteToMove and squares[2] == 7)):
                                if whiteToMove:
                                    Graphics.pawn_promotion_square(screen, squares[2], squares[3], self.pieces["wB"], self.pieces["wN"], self.pieces["wR"], self.pieces["wQ"], colour)
                                else:
                                    Graphics.pawn_promotion_square(screen, squares[2], squares[3], self.pieces["bB"], self.pieces["bN"], self.pieces["bR"], self.pieces["bQ"], colour)
                                promotion = True
                                if whiteToMove:
                                    promotionTurn = True
                                else:
                                    promotionTurn = False
                            else:
                                board[squares[2]][squares[3]] = board[squares[0]][squares[1]]
                                board[squares[0]][squares[1]] = "--"
                                if squares[0] == 0 and squares[1] == 0:
                                    moves.bRook1HasMoved = True
                                elif squares[0] == 0 and squares[1] == 7:
                                    moves.bRook2HasMoved = True
                                elif squares[0] == 0 and squares[1] == 4:
                                    moves.bKingHasMoved = True
                                elif squares[0] == 7 and squares[1] == 0:
                                    moves.wRook1HasMoved = True
                                elif squares[0] == 7 and squares[1] == 7:
                                    moves.wRook2HasMoved = True
                                elif squares[0] == 7 and squares[1] == 4:
                                    moves.wKingHasMoved = True
                            if not promotion:
                                squares = []
                                moveMade = True
                        else:
                            clicks = 0
                            squares = []

                    elif self.clicks == 1 and board[pos[1] // SQSIZE][pos[0] // SQSIZE][0] == allyColour:
                        squares = [pos[1] // SQSIZE, pos[0] // SQSIZE]

                    else:
                        for i in range(2):
                            squares.pop(-1)
            if moveMade:
                whiteToMove = not whiteToMove
                validMoves, inCheck = moves.getValidMoves(whiteToMove, board, previousMove, previousPiece)
                moveMade = False
                if validMoves == []:
                    if inCheck == True:
                        inCheckmate = True
                        whiteToMove = not whiteToMove
                    else:
                        inStalemate = True
                promotion = False



            Graphics.draw_squares(screen, colours[colour])
            Graphics.draw_pieces(screen, board, self.pieces)
            if self.clicks == 1:
                Graphics.show_highlights(screen, validMoves, squares)
            if promotion:
                whiteToMove = promotionTurn
                validMoves = []
                if whiteToMove:
                    Graphics.pawn_promotion_square(screen, squares[2], squares[3], self.pieces["wB"], self.pieces["wN"], self.pieces["wR"], self.pieces["wQ"], colour)
                else:
                    Graphics.pawn_promotion_square(screen, squares[2], squares[3], self.pieces["bB"], self.pieces["bN"], self.pieces["bR"], self.pieces["bQ"], colour)

            if inCheckmate:
                pygame.display.flip()
                self.checkmate(whiteToMove)
                running = False
            
            if inStalemate:
                pygame.display.flip()
                self.stalemate()
                running = False
            
            pygame.display.flip()         


main = Main()
main.main_loop()