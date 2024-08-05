from vars import *

class Moves:
    def __init__(self, board):
        self.ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, 
                            "5": 3, "6": 2, "7": 1, "8": 0}
        self.rowsToRanks = {v: k for k, v in self.ranksToRows.items()}
        self.filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, 
                            "e": 5, "f": 6, "g": 7, "h": 8}
        self.colsToFiles = {v: k for k, v in self.filesToCols.items()}

        for r in range(ROWSIZE):
            for c in range(COLSIZE):
                if board[r][c] == "wK":
                    self.wKingLocation = (r, c)
                elif board[r][c] == "bK":
                    self.bKingLocation = (r, c)

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
        possibleMoves = self.getAllPossibleMoves(whiteToMove, board)
        return possibleMoves


    def getAllPossibleMoves(self, whiteToMove, board):
        colour = "w" if whiteToMove else "b"
        moves = []
        for row in range(ROWSIZE):
            for col in range(COLSIZE):
                if board[row][col][0] == colour:
                    piece = board[row][col][1]
                    if piece == "p":
                        self.getPawnMoves(row, col, moves, board, colour)
                    elif piece == "N":
                        self.getKnightMoves(row, col, moves, board, colour)
                    elif piece == "B":
                        self.getBishopMoves(row, col, moves, board, colour)
                    elif piece == "R":
                        self.getRookMoves(row, col, moves, board, colour)
                    elif piece == "Q":
                        self.getQueenMoves(row, col, moves, board, colour)
                    elif piece == "K":
                        self.getKingMoves(row, col, moves, board, colour)
        return moves
    
    def getPawnMoves(self, r, c, moves, board, colour):
        if colour == "w":
            if board[r-1][c] == "--" and r != 0:
                moves.append(str(r) + str(c) + str(r-1) + str(c))
                if r == 6 and board[r-2][c] == "--":
                    moves.append(str(r) + str(c) + str(r-2) + str(c))
            if c != 0:
                if board[r-1][c-1] != "--" and board[r-1][c-1][0] != colour and r != 0:
                    moves.append(str(r) + str(c) + str(r-1) + str(c-1))
            if c != 7:
                if board[r-1][c+1] != "--" and board[r-1][c+1][0] != colour and r != 0:
                    moves.append(str(r) + str(c) + str(r-1) + str(c+1))

        else:
            if board[r+1][c] == "--" and r != 7:
                moves.append(str(r) + str(c) + str(r+1) + str(c))
                if r == 1 and board[r+2][c] == "--":
                    moves.append(str(r) + str(c) + str(r+2) + str(c))
            if c != 0:
                if board[r+1][c-1] != "--" and board[r+1][c-1][0] != colour and r != 0:
                    moves.append(str(r) + str(c) + str(r+1) + str(c-1))
            if c != 7:
                if board[r+1][c+1] != "--" and board[r+1][c+1][0] != colour and r != 0:
                    moves.append(str(r) + str(c) + str(r+1) + str(c+1))
            
            

    def getKnightMoves(self, r, c, moves, board, colour):
        directions = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2))
        enemyColour = "b" if colour == "w" else "w"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                if board[endRow][endCol] == "--" or board[endRow][endCol][0] == enemyColour:
                    moves.append(str(r) + str(c) + str(endRow) + str(endCol))


    def getBishopMoves(self, r, c, moves, board, colour):
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
                    elif endPiece[0] == enemyColour:
                        moves.append(str(r) + str(c) + str(endRow) + str(endCol))
                        break
                    else:
                        break
                else:
                    break

    def getRookMoves(self, r, c, moves, board, colour):
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
                    elif endPiece[0] == enemyColour:
                        moves.append(str(r) + str(c) + str(endRow) + str(endCol))
                        break
                    else:
                        break
                else:
                    break
                    
    def getQueenMoves(self, r, c, moves, board, colour):
        self.getRookMoves(r, c, moves, board, colour)
        self.getBishopMoves(r, c, moves, board, colour)

    def getKingMoves(self, r, c, moves, board, colour):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1))
        enemyColour = "b" if colour == "w" else "w"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                if board[endRow][endCol] == "--" or board[endRow][endCol][0] == enemyColour:
                    moves.append(str(r) + str(c) + str(endRow) + str(endCol))



    def searchForPinsAndChecks(self, kingLocation, board, whiteToMove):
        print(whiteToMove)
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1))
        allyColour = "w" if whiteToMove else "b"
        enemyColour = "w" if allyColour == "b" else "b"
        potentialPins = []
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
        return checks
        
        
    def findKnightChecks(self, kingLocation, board, enemyColour):
        checks = []
        directions = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2))
        for d in directions:
            try:
                if board[kingLocation[0] + d[0]][kingLocation[1] + d[1]] == (enemyColour + "N") and 0 <= (kingLocation[0] + d[0]) <= 7 and 0 <= (kingLocation[1] + d[1]) <= 7:
                    checks.append((kingLocation[0] + d[0], kingLocation[1] + d[1]))
                    print(checks)
            except IndexError:
                pass
        return checks
    
    def findPawnChecks(self, kingLocation, board, enemyColour):
        checks = []
        print(kingLocation)
        print(enemyColour)
        if enemyColour == 'w':
            if kingLocation[0] != 7:
                if kingLocation[1] != 7:
                    if board[kingLocation[0] + 1][kingLocation[1] + 1] == 'wp':
                        checks.append((kingLocation[0] + 1, kingLocation[1] + 1))
                        print("Check Found")
                        print(checks)
                if kingLocation[1] != 0:
                    if board[kingLocation[0] + 1][kingLocation[1] - 1] == 'wp':
                        checks.append((kingLocation[0] + 1, kingLocation[1] - 1))
                        print("Check Found")
                        print(checks)
        else:
            if kingLocation[0] != 0:
                if kingLocation[1] != 7:
                    if board[kingLocation[0] - 1][kingLocation[1] + 1] == 'bp':
                        checks.append((kingLocation[0] - 1, kingLocation[1] + 1))
                        print("Check Found")
                        print(checks)
                if kingLocation[1] != 0:
                    if board[kingLocation[0] - 1][kingLocation[1] - 1] == 'bp':
                        checks.append((kingLocation[0] - 1, kingLocation[1] - 1))
                        print("Check Found")
                        print(checks)
        
        return checks