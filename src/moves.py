from vars import *

class Moves:
    def __init__(self):
        self.ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, 
                            "5": 3, "6": 2, "7": 1, "8": 0}
        self.rowsToRanks = {v: k for k, v in self.ranksToRows.items()}
        self.filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, 
                            "e": 5, "f": 6, "g": 7, "h": 8}
        self.colsToFiles = {v: k for k, v in self.filesToCols.items()}

    def getValidMoves(self, whiteToMove, board):
        possibleMoves = self.getAllPossibleMoves(whiteToMove, board)
        return possibleMoves


    def getAllPossibleMoves(self, whiteToMove, board):
        turn = 'w' if whiteToMove else 'b'
        moves = []
        for row in range(ROWSIZE):
            for col in range(COLSIZE):
                if board[row][col][0] == turn:
                    piece = board[row][col][1]
                    if piece == 'p':
                        self.getPawnMoves(row, col, moves, board, turn)
                    elif piece == 'N':
                        self.getKnightMoves(row, col, moves, board)
                    elif piece == 'B':
                        self.getBishopMoves(row, col, moves, board)
                    elif piece == 'R':
                        self.getRookMoves(row, col, moves, board)
                    elif piece == 'Q':
                        self.getQueenMoves(row, col, moves, board)
                    elif piece == 'K':
                        self.getKingMoves(row, col, moves, board)
        return moves
    
    def getPawnMoves(self, r, c, moves, board, turn):
        print(turn)
        if turn == 'w':
            if board[r-1][c] == "--" and r != 0:
                moves.append(str(r) + str(c) + str(r-1) + str(c))
                if r == 6 and board[r-2][c] == "--":
                    moves.append(str(r) + str(c) + str(r-2) + str(c))
            if c != 0:
                if board[r-1][c-1] != "--" and board[r-1][c-1][0] != turn and r != 0:
                    moves.append(str(r) + str(c) + str(r-1) + str(c-1))
            if c != 7:
                if board[r-1][c+1] != "--" and board[r-1][c+1][0] != turn and r != 0:
                    moves.append(str(r) + str(c) + str(r-1) + str(c+1))

        else:
            if board[r+1][c] == "--" and r != 7:
                moves.append(str(r) + str(c) + str(r+1) + str(c))
                if r == 1 and board[r+2][c] == "--":
                    moves.append(str(r) + str(c) + str(r+2) + str(c))
            if c != 0:
                if board[r+1][c-1] != "--" and board[r+1][c-1][0] != turn and r != 0:
                    moves.append(str(r) + str(c) + str(r+1) + str(c-1))
            if c != 7:
                if board[r+1][c+1] != "--" and board[r+1][c+1][0] != turn and r != 0:
                    moves.append(str(r) + str(c) + str(r+1) + str(c+1))
            
            

    def getKnightMoves(self, r, c, moves, board):
        pass

    def getBishopMoves(self, r, c, moves, board):
        pass

    def getRookMoves(self, r, c, moves, board):
        pass

    def getQueenMoves(self, r, c, moves, board):
        pass

    def getKingMoves(self, r, c, moves, board):
        pass
