class Notation():
    def __init__(self):
        self.ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, 
                            "5": 3, "6": 2, "7": 1, "8": 0}
        self.rowsToRanks = {v: k for k, v in self.ranksToRows.items()}
        self.filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, 
                            "e": 4, "f": 5, "g": 6, "h": 7}
        self.colsToFiles = {v: k for k, v in self.filesToCols.items()}
    
    def toRankFile(self, moveLog, board, check, checkmate):
        RFNotation = ''
        move = moveLog[-1]
        moveLog.pop(-1)
        piece = board[int(move[0][0])][int(move[0][1])][1]
        if piece != 'p':
            RFNotation = RFNotation + piece
        else:
            if move[1] != '--':
                RFNotation = RFNotation + self.colsToFiles[int(move[0][1])]

        if move[1] != '--':
            RFNotation = RFNotation + 'x'
        RFNotation = RFNotation + str(self.colsToFiles[int(move[0][3])]) + str(self.rowsToRanks[int(move[0][2])])
        if check:
            if checkmate:
                RFNotation = RFNotation + "#"
            else:
                RFNotation = RFNotation + "+"
        moveLog.append(RFNotation)
        return moveLog