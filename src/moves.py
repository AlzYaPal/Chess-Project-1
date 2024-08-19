from vars import *
from chess_engine import *

class Moves:
    def __init__(self, board):
        self.engine = Engine()

        for r in range(ROWSIZE):
            for c in range(COLSIZE):
                if board[r][c] == "wK":
                    self.wKingLocation = (r, c)
                elif board[r][c] == "bK":
                    self.bKingLocation = (r, c)

        self.wKingHasMoved = self.bKingHasMoved = self.wRook1HasMoved = self.wRook2HasMoved = self.bRook1HasMoved = self.bRook2HasMoved = False

    def getKingLocation(self, whiteToMove, board):
        if whiteToMove:
            for r in range(ROWSIZE):
                for c in range(COLSIZE):
                    if board[r][c] == "wK":
                        return (r, c)
        else:
            for r in range(ROWSIZE):
                for c in range(COLSIZE):
                    if board[r][c] == "bK":
                        return (r, c)


    def getValidMoves(self, whiteToMove, board):
        engine = self.engine
        kingLocation = self.getKingLocation(whiteToMove, board)
        strKingLocation = str(kingLocation[0]) + str(kingLocation[1])
        moves = self.getAllPossibleMoves(whiteToMove, board, True)
        pins, checks = self.searchForPinsAndChecks(kingLocation, board, whiteToMove)
        inCheck = False

        format = []
        if checks != []:
            inCheck = True
            for check in checks:
                if check != []:
                    format.append(check[0])
            checks = format
            format = []
            if len(checks) == 1:
                check = checks[0]
                newBoard = board
                blockOrTake = []
                if kingLocation[0] == check[0]:
                    diffX = 0
                elif kingLocation[0] < check[0]:
                    diffX = -1
                else:
                    diffX = 1

                if kingLocation[1] == check[1]:
                    diffY = 0
                elif kingLocation[1] < check[1]:
                    diffY = -1
                else:
                    diffY = 1
                distance = [kingLocation[0] - check[0], kingLocation[1] - check[1]]
                
                absDistance = distance
                if distance[0] < 0:
                    absDistance[0] *= -1
                if distance[1] < 0:
                    absDistance[1] *= -1

                else:
                    absDistance = distance

                loopDistance = absDistance[0] if absDistance[0] != 0 else absDistance[1]

                for i in range(loopDistance):
                    blockOrTake.append(((diffX * i * distance[0] // absDistance[0]) + check[0], (diffY * i * distance[0] // absDistance[0]) + check[1]))

                for i in range(len(moves)):
                    move = moves[i]

                    if board[check[0]][check[1]][1] == "N":
                        blockOrTake = [check]

                    if move[0:2] == strKingLocation:
                        squares = [int(move[0]), int(move[1]), int(move[2]), int(move[3])]

                        engine.moveLog.append((move, board[squares[2]][squares[3]]))
                        newBoard[squares[2]][squares[3]] = newBoard[squares[0]][squares[1]]
                        newBoard[squares[0]][squares[1]] = "--"
                        newMoves = self.getAllPossibleMoves(not whiteToMove, newBoard, True)
                        move = engine.moveLog[-1]
                        move_squares = move[0]
                        piece = move[1]
                        board[int(move_squares[0])][int(move_squares[1])] = board[int(move_squares[2])][int(move_squares[3])]
                        board[int(move_squares[2])][int(move_squares[3])] = piece
                        engine.moveLog.pop(-1)
                        move_squares = []
                        for newMove in newMoves:
                            if newMove[2:4] == str(squares[2]) + str(squares[3]):
                                try:
                                    moves[moves.index(move[0])] = ''
                                except ValueError:
                                    pass
                        newBoard = board
                    
                    elif not ((int(move[2]), int(move[3])) in blockOrTake):
                        moves[moves.index(move)] = ''

            else:
                newBoard = board
                for i in range(len(moves)):
                    move = moves[i]
                    if move[0:2] == strKingLocation:
                        squares = [int(move[0]), int(move[1]), int(move[2]), int(move[3])]
                        engine.moveLog.append((move, board[squares[2]][squares[3]]))
                        newBoard[squares[2]][squares[3]] = newBoard[squares[0]][squares[1]]
                        newBoard[squares[0]][squares[1]] = "--"
                        newMoves = self.getAllPossibleMoves(not whiteToMove, newBoard, True)
                        move = engine.moveLog[-1]
                        move_squares = move[0]
                        piece = move[1]
                        board[int(move_squares[0])][int(move_squares[1])] = board[int(move_squares[2])][int(move_squares[3])]
                        board[int(move_squares[2])][int(move_squares[3])] = piece
                        engine.moveLog.pop(-1)
                        move_squares = []
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

        if pins != []:
            for pin in pins:
                if pin != []:
                    for singlePin in pin:
                        format.append(singlePin)
            pins = format
        
            for move in moves:
                for pin in pins:
                    if int(move[0]) == pin[0] and int(move[1]) == pin[1]:
                        squares = (move[0], move[1], move[2], move[3])
                        newBoard = board
                        engine.moveLog.append((move, board[int(squares[2])][int(squares[3])]))
                        newBoard[int(squares[2])][int(squares[3])] = board[int(squares[0])][int(squares[1])]
                        newBoard[int(squares[0])][int(squares[1])] = "--"
                        newMoves = self.getAllPossibleMoves(not whiteToMove, newBoard, True)
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
        counter = 0
        for i in range(len(moves)):
            try:
                if moves[i - counter] == '':
                    moves.pop(i - counter)
                    counter += 1
            except IndexError:
                break
        return moves, inCheck


    def getAllPossibleMoves(self, whiteToMove, board, checkKingMoves):
        colour = "w" if whiteToMove else "b"
        moves = []
        for row in range(ROWSIZE):
            for col in range(COLSIZE):
                if board[row][col][0] == colour:
                    piece = board[row][col][1]
                    if piece == "K":
                        self.getKingMoves(row, col, moves, board, colour, checkKingMoves)
                    elif piece == "p":
                        self.getPawnMoves(row, col, moves, board, colour, checkKingMoves)
                    elif piece == "N":
                        self.getKnightMoves(row, col, moves, board, colour, checkKingMoves)
                    elif piece == "B":
                        self.getBishopMoves(row, col, moves, board, colour, checkKingMoves)
                    elif piece == "R":
                        self.getRookMoves(row, col, moves, board, colour, checkKingMoves)
                    elif piece == "Q":
                        self.getQueenMoves(row, col, moves, board, colour, checkKingMoves)

                    self.castling(board, whiteToMove, moves)
        return moves
        
    def castling(self, board, whiteToMove, moves):
        long = short = False
        if whiteToMove:
            if not self.wKingHasMoved:
                if not self.wRook1HasMoved and board[7][1] == '--' and board[7][2] == '--' and board[7][3] == '--':
                    long = True
                if not self.wRook2HasMoved and board[7][5] == '--' and board[7][6] == '--':
                    short = True
        else:
            if not self.bKingHasMoved:
                if not self.bRook1HasMoved and board[0][1] == '--' and board[0][2] == '--' and board[0][3] == '--':
                    long = True
                if not self.bRook2HasMoved and board[0][5] == '--' and board[0][6] == '--':
                    short = True
        
        
        if whiteToMove and long:
            moves.append('7472')
        if whiteToMove and short:
            moves.append('7476')
        if not whiteToMove and long:
            moves.append('0402')
        if not whiteToMove and short:
            moves.append('0406')
        
    
    def getPawnMoves(self, r, c, moves, board, colour, checkKingMoves):
        if colour == "w":
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

        else:
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
            
            

    def getKnightMoves(self, r, c, moves, board, colour, checkKingMoves):
        directions = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2))
        enemyColour = "b" if colour == "w" else "w"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                if (board[endRow][endCol] == "--" or board[endRow][endCol][0] == enemyColour) or (not checkKingMoves and board[endRow][endCol][0] == colour):
                    moves.append(str(r) + str(c) + str(endRow) + str(endCol))


    def getBishopMoves(self, r, c, moves, board, colour, checkKingMoves):
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

    def getRookMoves(self, r, c, moves, board, colour, checkKingMoves):
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
                    
    def getQueenMoves(self, r, c, moves, board, colour, checkKingMoves):
        self.getRookMoves(r, c, moves, board, colour, checkKingMoves)
        self.getBishopMoves(r, c, moves, board, colour, checkKingMoves)

    def getKingMoves(self, r, c, moves, board, colour, checkKingMoves):
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
            for move in kingMoves:
                piece = board[int(move[2])][int(move[3])]
                newBoard[int(move[2])][int(move[3])] = 'wK' if colour == 'w' else 'bK'
                newBoard[r][c] = "--"
                newLocation = self.getKingLocation(True if colour == 'w' else False, newBoard)
                oppMoves = self.getAllPossibleMoves(True if colour == 'b' else False, newBoard, False)
                for oppMove in oppMoves:
                    if int(oppMove[2]) == int(newLocation[0]) and int(oppMove[3]) == int(newLocation[1]):
                        try:
                            moves.pop(moves.index(move))
                        except ValueError:
                            pass
                board[int(move[2])][int(move[3])] = piece
                board[int(move[0])][int(move[1])] = 'wK' if colour == 'w' else 'bK'




    def searchForPinsAndChecks(self, kingLocation, board, whiteToMove):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1))
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
        for i in range(COLSIZE):
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

        #if len(RCIPins[0]) == 1:
            #list(RCIPins[0]).insert(0, ())
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