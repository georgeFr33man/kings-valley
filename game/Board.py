import math
import sys


class Board:
    # Fields declaration
    emptyField = 0

    # Pawns and kings
    whitePawn = 2
    whiteKing = 3
    blackPawn = 4
    blackKing = 5

    # Board state
    __boardState = []

    def __init__(self, boardWidth, boardHeight):
        if boardWidth % 2 == 0 or boardHeight % 2 == 0:
            sys.exit("Both board width and board height must must be an odd number. Quitting...")
        else:
            self.boardWidth = boardWidth
            self.boardHeight = boardHeight
            self.__boardState = self.__createStarterBoard()
            self.kingsField = self.getKingsValleyFieldCords()

    def __createStarterBoard(self):
        boardState = self.createWhiteboard()
        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                if y == 0:
                    if x == math.floor(self.boardWidth / 2):
                        boardState[y][x] = self.whiteKing
                    else:
                        boardState[y][x] = self.whitePawn
                elif y == self.boardHeight - 1:
                    if x == math.floor(self.boardWidth / 2):
                        boardState[y][x] = self.blackKing
                    else:
                        boardState[y][x] = self.blackPawn
                else:
                    boardState[y][x] = self.emptyField

        return boardState

    def createWhiteboard(self):
        return [[self.emptyField] * self.boardWidth for i in range(self.boardHeight)]

    def printBoardState(self):
        for y in range(self.boardHeight):
            singleLine = ""
            for x in range(self.boardWidth):
                singleLine += "    " + str(self.__boardState[y][x])
            print(singleLine + "\n")

    def getKingsValleyFieldCords(self):
        return {"x": math.floor(self.boardWidth / 2), "y": math.floor(self.boardHeight / 2)}

    def getKingsCords(self):
        whiteKingX = [x for x in self.__boardState if self.whiteKing in x][0]
        blackKingX = [x for x in self.__boardState if self.blackKing in x][0]

        return {
            "whiteKing": {
                "x": whiteKingX.index(self.whiteKing),
                "y": self.__boardState.index(whiteKingX)
            },
            "blackKing": {
                "x": blackKingX.index(self.blackKing),
                "y": self.__boardState.index(blackKingX)
            }
        }

    def clearBoard(self):
        self.__boardState = self.createWhiteboard()

    def getFieldValue(self, x, y):
        if 0 <= x < self.boardWidth and 0 <= y < self.boardHeight:
            return self.__boardState[y][x]

        return -1

    def setFieldValue(self, x, y, val=None):
        if val is None:
            val = self.emptyField
        self.__boardState[y][x] = val

    def getBoardState(self):
        return self.__boardState
