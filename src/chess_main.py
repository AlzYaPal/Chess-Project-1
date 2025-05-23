#Importing the Libraries
import sys, pygame
from intro_screen import *
from chess_engine import *
from colours import *
from graphics import *
from moves import *
from notation import *
from vars import *

'''
This is resposible for pulling all the algorithms together and getting them all to work in the order required
'''

class Main:
    def __init__(self):
        pygame.init() #Initialise Pygame
        self.engine = Engine()
        self.screen = pygame.display.set_mode((width, height)) #Sets the board size with the width and height variables for vars.py
        self.board = self.engine.getBoard()

        # Dictionary to load the names and images (png) for all pieces
        self.pieces = {"wR": pygame.transform.scale(pygame.image.load("assets/pieces/wR.png"), (squareSize, squareSize)), #White Rook
                  "wN": pygame.transform.scale(pygame.image.load("assets/pieces/wN.png"), (squareSize, squareSize)), #White Knight
                  "wB": pygame.transform.scale(pygame.image.load("assets/pieces/wB.png"), (squareSize, squareSize)), #White Bishop
                  "wQ": pygame.transform.scale(pygame.image.load("assets/pieces/wQ.png"), (squareSize, squareSize)), #White Queen
                  "wK": pygame.transform.scale(pygame.image.load("assets/pieces/wK.png"), (squareSize, squareSize)), #White King
                  "wp": pygame.transform.scale(pygame.image.load("assets/pieces/wp.png"), (squareSize, squareSize)), #WHite Pawn
                  "bR": pygame.transform.scale(pygame.image.load("assets/pieces/bR.png"), (squareSize, squareSize)), #Black Rook
                  "bN": pygame.transform.scale(pygame.image.load("assets/pieces/bN.png"), (squareSize, squareSize)), #Black Knight
                  "bB": pygame.transform.scale(pygame.image.load("assets/pieces/bB.png"), (squareSize, squareSize)), #Black Bishop
                  "bQ": pygame.transform.scale(pygame.image.load("assets/pieces/bQ.png"), (squareSize, squareSize)), #Black Queen
                  "bK": pygame.transform.scale(pygame.image.load("assets/pieces/bK.png"), (squareSize, squareSize)), #Black King
                  "bp": pygame.transform.scale(pygame.image.load("assets/pieces/bp.png"), (squareSize, squareSize)), #Black Pawn
                  }
        self.clicks = 0
        self.squares = []
        self.whiteToMove = True

        # Added Icon and Caption
        pygame.display.set_icon(pygame.image.load("assets/icon/icon.png"))
    
    #Algorithm for if in checkmate
    def checkmate(self, whiteToMove):
        running = True
        font = pygame.font.Font("assets/font/dahliaregictik.ttf", 44)
        if whiteToMove:
            checkmateStr = font.render("White Wins By Checkmate!", True, (0, 0, 0))
            self.screen.blit(checkmateStr, (10, 268))
        else:
            checkmateStr = font.render("Black Wins By Checkmate!", True, (0, 0, 0))
            self.screen.blit(checkmateStr, (12, 268))
        pygame.display.flip()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            
    #Stalemate (No Legal Moves + Not In check)
    def stalemate(self, insufficientMaterial):
        font = pygame.font.Font("assets/font/dahliaregictik.ttf", 44)
        if insufficientMaterial:
            drawStr = font.render("Insufficient Material", True, (0, 0, 0))
            self.screen.blit(drawStr, (80, 278))
        else:
            stalemateStr = font.render("Draw By Stalemate!", True, (0, 0, 0))
            self.screen.blit(stalemateStr, (90, 278))
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


    #Main Game Loop
    def mainLoop(self):
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
            #Displays whose turn it is to move
            if whiteToMove:
                pygame.display.set_caption("Chess - White To Move")
            else:
                pygame.display.set_caption("Chess - Black To Move")
            screen.fill((255, 255, 255)) #Fill in the board with white
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #If X button clicked
                    running = False
                elif event.type == pygame.KEYDOWN: #If a key is pressed on the keyboard
                    if event.key == pygame.K_LCTRL: #If said key is the left Control Key
                        #Change the colour of the board
                        colour += 1
                        if colour == 12:
                            colour = 0
                    elif event.key == pygame.K_x: #If said key is 'x'
                        self.clicks = 0
                        squares = []
                elif event.type == pygame.MOUSEBUTTONDOWN: #If the mouse is clicked
                    pos = pygame.mouse.get_pos() #Gets the mouse position as a tuple
                    squares.append(pos[1] // squareSize)
                    squares.append(pos[0] // squareSize)
                    
                    if promotion: #If a pawn has reached the final rank
                        if ((0 <= pos[1] <= 75 and whiteToMove) or (525 <= pos[1] <= 600 and not whiteToMove)) and \
                            (squares[3] * squareSize) <= pos[0] < ((squares[3] + 1) * squareSize):
                            if whiteToMove:
                                #Promoted to Queen
                                if pos[1] <= 37.5 and pos[0] - (squares[3] * squareSize) <= 37.5:
                                    board[squares[2]][squares[3]] = 'wQ'
                                    board[squares[0]][squares[1]] = '--'
                                #Underpromoted to Knight
                                elif pos[1] <= 37.5 and 37.5 <= pos[0] - (squares[3] * squareSize) < 75:
                                    board[squares[2]][squares[3]] = 'wN'
                                    board[squares[0]][squares[1]] = '--'
                                #Underpromoted to Rook
                                elif 37.5 <= pos[1] - (squares[2] * squareSize) < 75 and pos[0] - (squares[3] * squareSize) <= 37.5:
                                    board[squares[2]][squares[3]] = 'wR'
                                    board[squares[0]][squares[1]] = '--'
                                #Underpromoted to Bishop
                                else:
                                    board[squares[2]][squares[3]] = 'wB'
                                    board[squares[0]][squares[1]] = '--'
                            else:
                                #Same basis as for white
                                if pos[1] >= 562.5 and pos[0] - (squares[3] * squareSize) <= 37.5:
                                    board[squares[2]][squares[3]] = 'bB'
                                    board[squares[0]][squares[1]] = '--'
                                elif pos[1] <= 562.5 and 37.5 <= pos[0] - (squares[3] * squareSize) < 75:
                                    board[squares[2]][squares[3]] = 'bR'
                                    board[squares[0]][squares[1]] = '--'
                                elif 562.5 <= pos[1] - (squares[2] * squareSize) < 525 and pos[0] - (squares[3] * squareSize) <= 37.5:
                                    board[squares[2]][squares[3]] = 'bN'
                                    board[squares[0]][squares[1]] = '--'
                                else:
                                    board[squares[2]][squares[3]] = 'bQ'
                                    board[squares[0]][squares[1]] = '--'
                            moveMade = True
                            engine.RFMoveLog[-1] = engine.RFMoveLog[-1] + "=" + board[squares[2]][squares[3]][1]
                            

                    
                    if board[squares[-2]][squares[-1]] != "--" and self.clicks == 0 and not promotion: #If a piece has been selected and pawn promotion is NOT taking place
                        self.clicks = 1
                        allyColour = 'w' if whiteToMove else 'b'
                    elif self.clicks == 1 and board[pos[1] // squareSize][pos[0] // squareSize][0] != allyColour: #If a possible move is made
                        self.clicks = 0
                        move = str(squares[0]) + str(squares[1]) + str(squares[2]) + str(squares[3])
                        if move in validMoves: #|If the selected move is valid
                            engine.moveLog.append((move, board[squares[2]][squares[3]]))
                            previousMove = engine.moveLog[-1]
                            engine.RFMoveLog = (notation.toRankFile(engine.moveLog, board, inCheck, inCheckmate))
                            previousPiece = board[squares[0]][squares[1]][1]
                            if move == '0402': #Long Castles for Black
                                board[0][4] = '--'
                                board[0][0] = '--'
                                board[0][2] = 'bK'
                                board[0][3] = 'bR'
                                moves.bKingHasMoved = True
                                moves.bRook1HasMoved = True
                            elif move == '0406': #Short Castles for Black
                                board[0][4] = '--'
                                board[0][7] = '--'
                                board[0][6] = 'bK'
                                board[0][5] = 'bR'
                                moves.bKingHasMoved = True
                                moves.bRook2HasMoved = True
                            elif move == '7472': #Long Castles for White
                                board[7][4] = '--'
                                board[7][0] = '--'
                                board[7][2] = 'wK'
                                board[7][3] = 'wR'
                                moves.wKingHasMoved = True
                                moves.wRook1HasMoved = True
                            elif move == '7476': #Short Castles for Black
                                board[7][4] = '--'
                                board[7][7] = '--'
                                board[7][6] = 'wK'
                                board[7][5] = 'wR'
                                moves.wKingHasMoved = True
                                moves.wRook2HasMoved = True
                            elif board[int(move[0])][int(move[1])][1] == 'p' and move[1] != move[3] and board[int(move[2])][int(move[3])] == '--': #If En Passant Played
                                board[squares[2]][squares[3]] = board[squares[0]][squares[1]]
                                board[squares[0]][squares[1]] = '--'
                                if whiteToMove:
                                    board[squares[2] + 1][squares[3]] = '--'
                                else:
                                    board[squares[2] - 1][squares[3]] = '--'

                            elif board[squares[0]][squares[1]][1] == 'p' and ((whiteToMove and squares[2] == 0) or (not whiteToMove and squares[2] == 7)): #If a pawn reaches the back rank (promotion)
                                board[squares[0]][squares[1]] = '--'
                                if whiteToMove:
                                    Graphics.pawnPromotionSquare(screen, squares[2], squares[3], self.pieces["wB"], self.pieces["wN"], self.pieces["wR"], self.pieces["wQ"], colour)
                                else:
                                    Graphics.pawnPromotionSquare(screen, squares[2], squares[3], self.pieces["bB"], self.pieces["bN"], self.pieces["bR"], self.pieces["bQ"], colour)
                                promotion = True
                                if whiteToMove:
                                    promotionTurn = True
                                else:
                                    promotionTurn = False
                            else:
                                board[squares[2]][squares[3]] = board[squares[0]][squares[1]]
                                board[squares[0]][squares[1]] = "--"
                                if squares[0] == 0 and squares[1] == 0: #If the A-File Black Rook has moved
                                    moves.bRook1HasMoved = True
                                elif squares[0] == 0 and squares[1] == 7: #If the H-file Black Rook has moved
                                    moves.bRook2HasMoved = True
                                elif squares[0] == 0 and squares[1] == 4: #If the Black King has moved
                                    moves.bKingHasMoved = True
                                elif squares[0] == 7 and squares[1] == 0: #If the A-File White Rook has moved
                                    moves.wRook1HasMoved = True
                                elif squares[0] == 7 and squares[1] == 7: #If the H-File White Rook has moved
                                    moves.wRook2HasMoved = True
                                elif squares[0] == 7 and squares[1] == 4: #If the White King has moved
                                    moves.wKingHasMoved = True
                            if not promotion:
                                squares = []
                                moveMade = True
                        else:
                            clicks = 0
                            squares = []

                    elif self.clicks == 1 and board[pos[1] // squareSize][pos[0] // squareSize][0] == allyColour:
                        squares = [pos[1] // squareSize, pos[0] // squareSize]

                    else:
                        for i in range(2):
                            squares.pop(-1)
            if moveMade:
                insufficientMaterial = False
                whiteToMove = not whiteToMove #Switch whose turn it is
                validMoves, inCheck = moves.getValidMoves(whiteToMove, board, previousMove, previousPiece) #Find all the valid moves in the position
                moveMade = False
                if validMoves == []: #Is it checkmate or stalemate or neither?
                    if inCheck == True:
                        inCheckmate = True
                        whiteToMove = not whiteToMove
                    else:
                        inStalemate = True
                remainingPieces = [] #Checking for a draw by insufficient material
                for row in range(rowSize):
                    for col in range(colSize):
                        if board[row][col] != "--":
                            remainingPieces.append(board[row][col])
                if len(remainingPieces) == 2: #Only Kings left
                    inStalemate = True
                    insufficientMaterial = True
                elif len(remainingPieces) == 3: #Both Kings and a Knight or Bishop on one side
                    for piece in remainingPieces:
                        if piece == 'wN' or piece == 'wB' or piece == 'bN' or piece == 'bB':
                            inStalemate = True
                            insufficientMaterial = True
                elif len(remainingPieces) == 4: #Both Kings and two knights, two bishops or a knight and a bishop
                    if ('wB' in remainingPieces and 'bN' in remainingPieces) or ('bB' in remainingPieces and 'wN' in remainingPieces) or ('wB' in remainingPieces and 'bB' in remainingPieces) or ('wN' in remainingPieces and 'bN' in remainingPieces):
                        inStalemate = True
                        insufficientMaterial = True
                        pass
                    knightCount = 0
                    for piece in remainingPieces:
                        if piece[1] == 'N':
                            knightCount += 1
                    if knightCount == 2:
                        inStalemate = True
                        insufficientMaterial = True
                elif len(remainingPieces) == 5: #Both Kings, two Knights on one side and either a Knight or a Bishop on the other
                    wKnightCount = 0
                    bKnightCount = 0
                    for piece in remainingPieces:
                        if piece == 'wN' and wKnightCount == 2:
                            wKnightCount += 1
                        elif piece == 'bN' and bKnightCount == 2:
                            bKnightCount += 1
                        elif piece[1] != 'K':
                            otherPiece = piece
                    if (wKnightCount == 2 and (otherPiece == 'bN' or otherPiece == 'bB') or bKnightCount == 2 and (otherPiece == 'wN' or otherPiece == 'wB')):
                        inStalemate = True
                        insufficientMaterial = True
                elif len(remainingPieces) == 6: #Both Kings and two knights on both sides
                    wKnightCount = 0
                    bKnightCount = 0
                    for piece in remainingPieces:
                        if piece == 'wN':
                            wKnightCount += 1
                        elif piece == 'bN':
                            bKnightCount += 1
                    if wKnightCount == 2 and bKnightCount == 2:
                        inStalemate = True
                        insufficientMaterial = True
                promotion = False


            #Setting up the board and pieces
            Graphics.drawSquares(screen, colours[colour])
            Graphics.drawPieces(screen, board, self.pieces)
            if self.clicks == 1:
                Graphics.showHighlights(screen, validMoves, squares) #Highlights the squares if a piece is selected
            if promotion: #Sets up the Pawn Promotion Variables
                whiteToMove = promotionTurn
                validMoves = []
                if whiteToMove:
                    Graphics.pawnPromotionSquare(screen, squares[2], squares[3], self.pieces["wB"], self.pieces["wN"], self.pieces["wR"], self.pieces["wQ"], colour)
                else:
                    Graphics.pawnPromotionSquare(screen, squares[2], squares[3], self.pieces["bB"], self.pieces["bN"], self.pieces["bR"], self.pieces["bQ"], colour)
            
            #Checkmate
            if inCheckmate:
                self.checkmate(whiteToMove)
                running = False
            
            #Stalemate
            if inStalemate:
                pygame.display.flip()
                running = self.stalemate(insufficientMaterial)
                running = False
            
            pygame.display.flip()         

#Running the Main Loop
main = Main()
main.mainLoop()

#Closes the program
pygame.quit()
sys.exit()
