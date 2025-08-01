from chess_engine import *
from vars import *

'''
This class is responsible for finding any possible moves for all pieces and
weeding out any illegal moves (i.e. any that would put their own King in check)
'''

class Moves:
    def __init__(self, board):
        self.engine = Engine()

        #Original Location of the Kings
        for row in range(rowSize):
            for col in range(colSize):
                if board[row][col] == "wK":
                    self.wKingLocation = (row, col)
                elif board[row][col] == "bK":
                    self.bKingLocation = (row, col)

        #Sets the castling condition variables all to false (i.e. the Kings can castle if there are no pieces in the way)
        self.wKingHasMoved = self.bKingHasMoved = self.wRook1HasMoved = self.wRook2HasMoved = self.bRook1HasMoved = self.bRook2HasMoved = False

    #Gets the location of the King of the side who are moving this go
    def getKingLocation(self, whiteToMove, board):
        if whiteToMove:
            for row in range(rowSize):
                for col in range(colSize):
                    if board[row][col] == "wK":
                        return (row, col)
        else:
            for row in range(rowSize):
                for col in range(colSize):
                    if board[row][col] == "bK":
                        return (row, col)

    #Calls the getAllPossibleMoves function and removes any illegal moves
    def getValidMoves(self, whiteToMove, board, moveLog, prevPiece):
        engine = self.engine
        kingLocation = self.getKingLocation(whiteToMove, board) #Gets the location of the King
        strKingLocation = str(kingLocation[0]) + str(kingLocation[1]) #Converts the location to a string
        moves = self.getAllPossibleMoves(whiteToMove, board, True, moveLog, prevPiece) #Gets every possible moves (negating checks and pins)
        pins, checks = self.searchForPinsAndChecks(kingLocation, board, whiteToMove) #Searches for all pins and checks being given
        inCheck = False

        format = []
        if checks != []: #If the king is currently in check
            inCheck = True
            for check in checks:
                if check != []: #I was getting a bug where I would get empty spaces in the checks array, so I changed it 
                                #to remove any 'checks' that were an empty list
                    format.append(check[0])
            checks = format
            format = []
            if len(checks) == 1: #If the King is in check from one piece
                check = checks[0] #Formats the list so that it is 1D
                newBoard = board
                blockOrTake = []
                if kingLocation[0] == check[0]: #Finding the direction and the distance of the checking piece from the King (Horizontal)
                    diffX = 0
                elif kingLocation[0] < check[0]:
                    diffX = -1
                else:
                    diffX = 1

                if kingLocation[1] == check[1]: #Finding the direction and the distance of the checking piece from the King (Vertical)
                    diffY = 0
                elif kingLocation[1] < check[1]:
                    diffY = -1
                else:
                    diffY = 1
                distance = [kingLocation[0] - check[0], kingLocation[1] - check[1]]
                
                absDistance = distance #Setting the absolute distance so that the blockOrTake list can be appended properly
                if distance[0] < 0:
                    absDistance[0] *= -1
                if distance[1] < 0:
                    absDistance[1] *= -1

                else:
                    absDistance = distance

                loopDistance = absDistance[0] if absDistance[0] != 0 else absDistance[1]

                for i in range(loopDistance): #Adding the squares on which the check can be blocked or the checking piece can be taken
                    if distance[0] == 0:
                        absDistance[0] = 1
                    if distance[1] == 0:
                        absDistance[1] = 1
                    blockOrTake.append(((diffX * i * distance[0] // absDistance[0]) + check[0], (diffY * i * distance[0] // absDistance[0]) + check[1]))

                for i in range(len(moves)):
                    move = moves[i]

                    if board[check[0]][check[1]][1] == "N":
                        blockOrTake = [check]

                    if move[0:2] == strKingLocation: #Checking for King moves (ensuring that the King can't take a piece that would mean that he would be in check)
                        squares = [int(move[0]), int(move[1]), int(move[2]), int(move[3])]

                        engine.moveLog.append((move, board[squares[2]][squares[3]]))
                        newBoard[squares[2]][squares[3]] = newBoard[squares[0]][squares[1]] #Making the move in question to check its validity
                        newBoard[squares[0]][squares[1]] = "--"
                        newMoves = self.getAllPossibleMoves(not whiteToMove, newBoard, True, '', '')
                        move = engine.moveLog[-1]
                        moveSquares = move[0]
                        piece = move[1]
                        board[int(moveSquares[0])][int(moveSquares[1])] = board[int(moveSquares[2])][int(moveSquares[3])]
                        board[int(moveSquares[2])][int(moveSquares[3])] = piece
                        engine.moveLog.pop(-1)
                        moveSquares = []
                        for newMove in newMoves:
                            if newMove[2:4] == str(squares[2]) + str(squares[3]):
                                try:
                                    moves[moves.index(move[0])] = ''
                                except ValueError:
                                    pass
                        newBoard = board
                    
                    elif not ((int(move[2]), int(move[3])) in blockOrTake):
                        moves[moves.index(move)] = ''

            else: #If the King is in check from two pieces (Double Check)
                newBoard = board
                for i in range(len(moves)):
                    move = moves[i]
                    if move[0:2] == strKingLocation: #Checking King moves again - two checks mean that blocking or taking is not possible as the King would still be in check from the other piece
                        squares = [int(move[0]), int(move[1]), int(move[2]), int(move[3])]
                        engine.moveLog.append((move, board[squares[2]][squares[3]]))
                        newBoard[squares[2]][squares[3]] = newBoard[squares[0]][squares[1]]
                        newBoard[squares[0]][squares[1]] = "--"
                        newMoves = self.getAllPossibleMoves(not whiteToMove, newBoard, True, '', '')
                        move = engine.moveLog[-1]
                        moveSquares = move[0]
                        piece = move[1]
                        board[int(moveSquares[0])][int(moveSquares[1])] = board[int(moveSquares[2])][int(moveSquares[3])]
                        board[int(moveSquares[2])][int(moveSquares[3])] = piece
                        engine.moveLog.pop(-1)
                        moveSquares = []
                        for newMove in newMoves:
                            if newMove[2:4] == str(squares[2]) + str(squares[3]):
                                moves[moves.index(move[0])] = ''
                        newBoard = board
                    else:
                        moves[moves.index(move)] = ''

        counter = 0
        for i in range(len(moves)):
            try:
                if moves[i - counter] == '':
                    moves.pop(i - counter)
                    counter += 1
            except IndexError:
                break

        if pins != []: #Formatting the Pins List
            for pin in pins:
                if pin != []:
                    for singlePin in pin:
                        format.append(singlePin)
            pins = format
        
            for move in moves: #Removing moves if the piece is pinned and the move would put the King in check
                for pin in pins:
                    if int(move[0]) == pin[0] and int(move[1]) == pin[1]:
                        squares = (move[0], move[1], move[2], move[3])
                        newBoard = board
                        engine.moveLog.append((move, board[int(squares[2])][int(squares[3])]))
                        newBoard[int(squares[2])][int(squares[3])] = board[int(squares[0])][int(squares[1])]
                        newBoard[int(squares[0])][int(squares[1])] = "--"
                        newMoves = self.getAllPossibleMoves(not whiteToMove, newBoard, True, '', '')
                        for newMove in newMoves:
                            if newMove[2:4] == str(kingLocation[0]) + str(kingLocation[1]):
                                moves[moves.index(move)] = ''
                                break
                        move = engine.moveLog[-1]
                        squares = move[0]
                        piece = move[1]
                        newBoard[int(squares[0])][int(squares[1])] = newBoard[int(squares[2])][int(squares[3])]
                        board[int(squares[2])][int(squares[3])] = piece
                        engine.moveLog.pop(-1)
                        squares = []
        #Formatting the List
        counter = 0
        for i in range(len(moves)):
            try:
                if moves[i - counter] == '':
                    moves.pop(i - counter)
                    counter += 1
            except IndexError:
                break
        self.castling(board, whiteToMove, moves, inCheck, self.getAllPossibleMoves(not whiteToMove, board, False, moveLog, prevPiece)) #Checking if castling is an available move
        return moves, inCheck


    def getAllPossibleMoves(self, whiteToMove, board, checkKingMoves, moveLog, prevPiece): #Finds all the moves that can be made, irrespective of checks and pins
        colour = "w" if whiteToMove else "b"
        moves = []
        for row in range(rowSize): #Iterating through the board and finding all possible moves for whatever piece is there
            for col in range(colSize):
                if board[row][col][0] == colour:
                    piece = board[row][col][1]
                    if piece == "K":
                        self.getKingMoves(row, col, moves, board, colour, checkKingMoves)
                    elif piece == "p":
                        self.getPawnMoves(row, col, moves, board, colour, checkKingMoves, moveLog, prevPiece)
                    elif piece == "N":
                        self.getKnightMoves(row, col, moves, board, colour, checkKingMoves)
                    elif piece == "B":
                        self.getBishopMoves(row, col, moves, board, colour, checkKingMoves)
                    elif piece == "R":
                        self.getRookMoves(row, col, moves, board, colour, checkKingMoves)
                    elif piece == "Q":
                        self.getQueenMoves(row, col, moves, board, colour, checkKingMoves)
        return moves
        
    def castling(self, board, whiteToMove, moves, inCheck, enemyMoves): #Can the King castle?
        kingPos = self.getKingLocation(whiteToMove, board)
        long = short = False
        if whiteToMove:
            initialKingPos = (7, 4)
            rCoord = '7'
            if not (self.wKingHasMoved or inCheck):
                if not self.wRook1HasMoved and board[7][1] == '--' and board[7][2] == '--' and board[7][3] == '--': #Checks if Long Castle is possible for White
                    long = True
                if not self.wRook2HasMoved and board[7][5] == '--' and board[7][6] == '--': #Checks if Short Castle is possible for White
                    short = True
            
        else:
            initialKingPos = (0, 4)
            rCoord = '0'
            if not (self.bKingHasMoved or inCheck):
                if not self.bRook1HasMoved and board[0][1] == '--' and board[0][2] == '--' and board[0][3] == '--':#Checks if Long Castle is possible for Black
                    long = True
                if not self.bRook2HasMoved and board[0][5] == '--' and board[0][6] == '--':#Checks if Short Castle is possible for Black
                    short = True
        
        for move in enemyMoves:
            if (move[2] == rCoord and (move[3] == '5' or move[3] == '6')):
                short = False
            if (move[2] == rCoord and (move[3] == '2' or move[3] == '3')):
                long = False
         #Adding the moves to the moves list
        if kingPos == initialKingPos:
            if whiteToMove and long:
                moves.append('7472')
            if whiteToMove and short:
                moves.append('7476')
            if not whiteToMove and long:
                moves.append('0402')
            if not whiteToMove and short:
                moves.append('0406')
        
    
    def getPawnMoves(self, r, c, moves, board, colour, checkKingMoves, moveLog, prevPiece): #Gets the moves for whichever pawn is being checked
        enPassant = ''
        if prevPiece == 'p' and (int(moveLog[0][2]) - int(moveLog[0][0]) == 2 or int(moveLog[0][2]) - int(moveLog[0][0]) == -2): #Checks for En Passant
            enPassant = [moveLog[0][2], moveLog[0][3]]
        if colour == "w": #Finds pawn moves for white pawns
            if board[r-1][c] == "--" and r != 0:
                moves.append(str(r) + str(c) + str(r-1) + str(c))
                if r == 6 and board[r-2][c] == "--":
                    moves.append(str(r) + str(c) + str(r-2) + str(c))
            if c != 0:
                if (board[r-1][c-1] != "--" and board[r-1][c-1][0] != colour and r != 0) or (not checkKingMoves and board[r-1][c-1][0] == colour):
                    moves.append(str(r) + str(c) + str(r-1) + str(c-1))
            if c != 7:
                if (board[r-1][c+1] != "--" and board[r-1][c+1][0] != colour and r != 0) or (not checkKingMoves and board[r-1][c+1][0] == colour):
                    moves.append(str(r) + str(c) + str(r-1) + str(c+1))
            if enPassant != '':
                if r == int(enPassant[0]) and  c == int(enPassant[1]) + 1:
                    moves.append(str(r) + str(c) + str(r - 1) + str(c - 1))
                elif r == int(enPassant[0]) and  c == int(enPassant[1]) - 1:
                    moves.append(str(r) + str(c) + str(r - 1) + str(c + 1))

        else: #Finds pawn moves for black pawns
            if board[r+1][c] == "--" and r != 7:
                moves.append(str(r) + str(c) + str(r+1) + str(c))
                if r == 1 and board[r+2][c] == "--":
                    moves.append(str(r) + str(c) + str(r+2) + str(c))
            if c != 0:
                if (board[r+1][c-1] != "--" and board[r+1][c-1][0] != colour and r != 0) or (not checkKingMoves and board[r+1][c-1][0] == colour):
                    moves.append(str(r) + str(c) + str(r+1) + str(c-1))
            if c != 7:
                if (board[r+1][c+1] != "--" and board[r+1][c+1][0] != colour and r != 0) or (not checkKingMoves and board[r+1][c+1][0] == colour):
                    moves.append(str(r) + str(c) + str(r+1) + str(c+1))
            if prevPiece == 'p':

                if int(moveLog[0][3]) != 0:
                    if int(moveLog[0][0]) - int(moveLog[0][2]) == 2 and board[int(moveLog[0][2])][int(moveLog[0][3]) - 1] == 'bp':
                        moves.append(str(r) + str(c) + str(r + 1) + str(c + 1))
                if int(moveLog[0][3]) != 7:
                    if int(moveLog[0][0]) - int(moveLog[0][2]) == 2 and board[int(moveLog[0][2])][int(moveLog[0][3]) + 1] == 'bp':
                        moves.append(str(r) + str(c) + str(r + 1) + str(c - 1))
            
            

    def getKnightMoves(self, r, c, moves, board, colour, checkKingMoves): #Finds the moves for whichever knight is being checked
        directions = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2))
        enemyColour = "b" if colour == "w" else "w"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                if (board[endRow][endCol] == "--" or board[endRow][endCol][0] == enemyColour) or (not checkKingMoves and board[endRow][endCol][0] == colour):
                    moves.append(str(r) + str(c) + str(endRow) + str(endCol))


    def getBishopMoves(self, r, c, moves, board, colour, checkKingMoves): #Finds the moves for whichever bishop is being checked
        directions = ((1, 1), (-1, 1), (-1, -1), (1, -1))
        enemyColour = "b" if colour == "w" else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(str(r) + str(c) + str(endRow) + str(endCol))
                    elif endPiece[0] == enemyColour  or (not checkKingMoves and endPiece[0] == colour):
                        moves.append(str(r) + str(c) + str(endRow) + str(endCol))
                        break
                    else:
                        break

                else:
                    break

    def getRookMoves(self, r, c, moves, board, colour, checkKingMoves): #Finds the moves for whichever rook is being checked
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        enemyColour = "b" if colour == "w" else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(str(r) + str(c) + str(endRow) + str(endCol))
                    elif endPiece[0] == enemyColour  or (not checkKingMoves and endPiece[0] == colour):
                        moves.append(str(r) + str(c) + str(endRow) + str(endCol))
                        break
                    else:
                        break

                else:
                    break
                    
    def getQueenMoves(self, r, c, moves, board, colour, checkKingMoves): #Finds the moves for the Queen
        self.getRookMoves(r, c, moves, board, colour, checkKingMoves)
        self.getBishopMoves(r, c, moves, board, colour, checkKingMoves)

    def getKingMoves(self, r, c, moves, board, colour, checkKingMoves): #Finds the moves for the King
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1))
        enemyColour = "b" if colour == "w" else "w"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                if board[endRow][endCol] == "--" or board[endRow][endCol][0] == enemyColour:
                    moves.append(str(r) + str(c) + str(endRow) + str(endCol))
        if checkKingMoves:
            newBoard = board
            piece = ''
            kingMoves = []
            for move in moves:
                if int(move[0]) == r and int(move[1]) == c:
                    kingMoves.append(move)
            for move in kingMoves: #Removing the moves that put the King into check
                piece = board[int(move[2])][int(move[3])]
                newBoard[int(move[2])][int(move[3])] = 'wK' if colour == 'w' else 'bK'
                newBoard[r][c] = "--"
                newLocation = self.getKingLocation(True if colour == 'w' else False, newBoard)
                oppMoves = self.getAllPossibleMoves(True if colour == 'b' else False, newBoard, False, '', '')
                for oppMove in oppMoves:
                    if int(oppMove[2]) == int(newLocation[0]) and int(oppMove[3]) == int(newLocation[1]):
                        try:
                            moves.pop(moves.index(move))
                        except ValueError:
                            pass
                board[int(move[2])][int(move[3])] = piece
                board[int(move[0])][int(move[1])] = 'wK' if colour == 'w' else 'bK'




    def searchForPinsAndChecks(self, kingLocation, board, whiteToMove):
        allyColour = "w" if whiteToMove else "b"
        enemyColour = "w" if allyColour == "b" else "b"
        checks = []
        pins = []
        try:
            checks.append(self.findKnightChecks(kingLocation, board, enemyColour))
            if checks == [[]]:
                checks = []
        except TypeError:
            pass
        checks.append(self.findPawnChecks(kingLocation, board, enemyColour))
        if checks == [[]]:
            checks = []
        RQPins, RQChecks = self.findRookQueenChecks(kingLocation, board, allyColour, enemyColour)
        checks.append(RQChecks)
        if pins == [[]]:
            pins = []
        pins.append(RQPins)
        if checks == [[]]:
            checks = []
        BQPins, BQChecks = self.findBishopQueenChecks(kingLocation, board, allyColour, enemyColour)
        pins.append(BQPins)
        if pins == [[], []]:
            pins = []
        checks.append(BQChecks)
        if checks == [[]]:
            checks = []
        return pins, checks
        
        
    def findKnightChecks(self, kingLocation, board, enemyColour):
        checks = []
        directions = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2))
        for d in directions:
            try:
                if board[kingLocation[0] + d[0]][kingLocation[1] + d[1]] == (enemyColour + "N") and 0 <= (kingLocation[0] + d[0]) <= 7 and 0 <= (kingLocation[1] + d[1]) <= 7:
                    checks.append((kingLocation[0] + d[0], kingLocation[1] + d[1]))
            except IndexError:
                pass
        return checks
    
    def findPawnChecks(self, kingLocation, board, enemyColour):
        checks = []
        if enemyColour == 'w':
            if kingLocation[0] != 7:
                if kingLocation[1] != 7:
                    if board[kingLocation[0] + 1][kingLocation[1] + 1] == 'wp':
                        checks.append((kingLocation[0] + 1, kingLocation[1] + 1))
                if kingLocation[1] != 0:
                    if board[kingLocation[0] + 1][kingLocation[1] - 1] == 'wp':
                        checks.append((kingLocation[0] + 1, kingLocation[1] - 1))
        else:
            if kingLocation[0] != 0:
                if kingLocation[1] != 7:
                    if board[kingLocation[0] - 1][kingLocation[1] + 1] == 'bp':
                        checks.append((kingLocation[0] - 1, kingLocation[1] + 1))
                if kingLocation[1] != 0:
                    if board[kingLocation[0] - 1][kingLocation[1] - 1] == 'bp':
                        checks.append((kingLocation[0] - 1, kingLocation[1] - 1))
        return checks

    def findRookQueenChecks(self, kingLocation, board, allyColour, enemyColour):
        RCIChecks = []
        RCIPins = []
        checks = []
        potentialPins = []
        pins = []
        r = kingLocation[0]
        c = kingLocation[1]
        boardRow = board[r]
        boardCol = []
        for i in range(colSize):
            boardCol.append(board[i][c])
        boardRowLeft = boardRow[:c + 1]
        boardRowRight = boardRow[c:]
        boardColLeft = boardCol[:r +1]
        boardColRight = boardCol[r:]
        boardRowLeftReorder = []
        boardColLeftReorder = []
        for i in range(len(boardRowLeft)):
            index = -1 * (i + 1)
            boardRowLeftReorder.append(boardRowLeft[index])
        for i in range(len(boardColLeft)):
            index = -1 * (i + 1)
            boardColLeftReorder.append(boardColLeft[index])

        boardRowLeft = boardRowLeftReorder
        boardColLeft = boardColLeftReorder
        RCIndex = [boardRowLeft, boardRowRight, boardColLeft, boardColRight]
        for i in range(len(RCIndex)):
            alliesFound = 0
            for j in range(1, len(RCIndex[i])):
                if RCIndex[i][j][0] == allyColour:
                    if alliesFound == 0:
                        alliesFound = 1
                        potentialPins.append((i, j))
                    else:
                        potentialPins = []
                        break
                elif RCIndex[i][j][0] == enemyColour and (RCIndex[i][j][1] == 'R' or RCIndex[i][j][1] == 'Q'):
                    if alliesFound == 1:
                        RCIPins.append(potentialPins)
                        potentialPins = []
                    else:
                        RCIChecks.append([i, j])
                elif RCIndex[i][j][0] == enemyColour and not (RCIndex[i][j][1] == 'R' or RCIndex[i][j][1] == 'Q'):
                    break

        if RCIPins != []:
            for i in range(len(RCIPins)):
                pin = RCIPins[i]
                pin = pin[0]
                if pin[0] == 0:
                    pins.append((r, c - pin[1]))
                elif pin[0] == 1:
                    pins.append((r, c + pin[1]))
                elif pin[0] == 2:
                    pins.append((r - pin[1], c))
                else:
                    pins.append((r + pin[1], c))
        if RCIChecks != []:
            check = RCIChecks[0]
            if check[0] == 0:
                checks.append((r, c - check[1]))
            elif check[0] == 1:
                checks.append((r, c + check[1]))
            elif check[0] == 2:
                checks.append((r - check[1], c))
            else:
                checks.append((r + check[1], c))
        return pins, checks

    def findBishopQueenChecks(self, kingLocation, board, allyColour, enemyColour):
        RCIChecks = []
        RCIPins = []
        checks = []
        potentialPins = []
        pins = []
        directions = ((1, 1), (-1, -1), (1, -1), (-1, 1))
        r = kingLocation[0]
        c = kingLocation[1]
        diagonal1Left = []
        diagonal1Right = []
        diagonal2Left = []
        diagonal2Right = []
        for d in directions:
            for i in range(8):
                if 0 <= r + (d[0] * i) <= 7 and 0 <= c + (d[1] * i) <= 7:
                    if d == directions[0]:
                        diagonal1Right.append((board[r + (d[0] * i)][c + (d[1] * i)]))
                    elif d == directions[1]:
                        diagonal1Left.append((board[r + (d[0] * i)][c + (d[1] * i)]))
                    elif d == directions[2]:
                        diagonal2Left.append((board[r + (d[0] * i)][c + (d[1] * i)]))
                    else:
                        diagonal2Right.append((board[r + (d[0] * i)][c + (d[1] * i)]))
                else:
                    break

        RCIndex = [diagonal1Left, diagonal1Right, diagonal2Left, diagonal2Right]
        for i in range(len(RCIndex)):
            alliesFound = 0
            for j in range(1, len(RCIndex[i])):
                if RCIndex[i][j][0] == allyColour:
                    if alliesFound == 0:
                        alliesFound = 1
                        potentialPins.append((i, j))
                    else:
                        potentialPins = []
                        break
                elif RCIndex[i][j][0] == enemyColour and (RCIndex[i][j][1] == 'B' or RCIndex[i][j][1] == 'Q'):
                    if alliesFound == 1:
                        RCIPins.append(potentialPins)
                        potentialPins = []
                    else:
                        RCIChecks.append([i, j])
                    break
                elif RCIndex[i][j][0] == enemyColour and not (RCIndex[i][j][1] == 'B' or RCIndex[i][j][1] == 'Q'):
                    break

        if RCIPins != []:
            if len(RCIPins[0]) == 1:
                x = 0
            else:
                x = 1
            for i in range(x, len(RCIPins[0])):
                pin = RCIPins[0][i]
                if pin[0] == 0:
                    pins.append((r - pin[1], c - pin[1]))
                elif pin[0] == 1:
                    pins.append((r + pin[1], c + pin[1]))
                elif pin[0] == 2:
                    pins.append((r + pin[1], c - pin[1]))
                else:
                    pins.append((r - pin[1], c + pin[1]))
        if RCIChecks != []:
            check = RCIChecks[0]
            if check[0] == 0:
                checks.append((r - check[1], c - check[1]))
            elif check[0] == 1:
                checks.append((r + check[1], c + check[1]))
            elif check[0] == 2:
                checks.append((r + check[1], c - check[1]))
            else:
                checks.append((r - check[1], c + check[1]))
        return pins, checks