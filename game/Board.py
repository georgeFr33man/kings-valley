import math
import sys

import game


class Board:
    # Fields declaration
    emptyField: int = 0

    # Pawns and kings
    whitePawn: int = 2
    whiteKing: int = 3
    blackPawn: int = 4
    blackKing: int = 5

    # Board state
    __boardState: list = []
    __cache: dict = {}

    def __init__(self, boardWidth: int, boardHeight: int):
        if boardWidth % 2 == 0 or boardHeight % 2 == 0:
            sys.exit("Both board width and board height must must be an odd number. Quitting...")
        else:
            self.boardWidth = boardWidth
            self.boardHeight = boardHeight
            self.clearCache()
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

                if boardState[y][x] != self.emptyField:
                    if isinstance(self.__cache[boardState[y][x]], list):
                        self.__cache[boardState[y][x]].append({"x": x, "y": y})
                    else:
                        self.__cache[boardState[y][x]] = {"x": x, "y": y}

        return boardState

    def createWhiteboard(self) -> list:
        return [[self.emptyField] * self.boardWidth for i in range(self.boardHeight)]

    def printBoardState(self):
        for y in range(self.boardHeight):
            singleLine = ""
            for x in range(self.boardWidth):
                singleLine += "    " + str(self.__boardState[y][x])
            print(singleLine + "\n")

    def getKingsValleyFieldCords(self) -> dict:
        return {"x": math.floor(self.boardWidth / 2), "y": math.floor(self.boardHeight / 2)}

    def getKingsCords(self) -> dict:
        return {
            self.whiteKing: self.__cache[self.whiteKing],
            self.blackKing: self.__cache[self.blackKing],
        }

    def clearBoard(self):
        self.__boardState = self.createWhiteboard()

    def restoreStarterBoard(self):
        self.clearCache()
        self.__boardState = self.__createStarterBoard()

    def getFieldValue(self, x: int, y: int):
        if 0 <= x < self.boardWidth and 0 <= y < self.boardHeight:
            return self.__boardState[int(y)][int(x)]

        return -1

    def setFieldValue(self, x: int, y: int, val=None):
        if val is None:
            val = self.emptyField
        self.__boardState[y][x] = val

    def getBoardState(self):
        return self.__boardState

    def move(self, move: 'game.Move.Move'):
        fieldValue = self.getFieldValue(move.moveFrom["x"], move.moveFrom["y"])
        self.setFieldValue(move.moveFrom["x"], move.moveFrom["y"], self.emptyField)
        self.setFieldValue(move.moveTo["x"], move.moveTo["y"], fieldValue)
        self.__updateCache(move)

    @classmethod
    def getPlayerPawns(cls, player: str):
        if game.Game.Game.whitePlayer == player:
            return [cls.whitePawn, cls.whiteKing]
        if game.Game.Game.blackPlayer == player:
            return [cls.blackPawn, cls.blackKing]

    def getCache(self) -> dict:
        return self.__cache

    def __updateCache(self, move: 'game.Move.Move'):
        fromX = move.moveFrom["x"]
        fromY = move.moveFrom["y"]
        toX = move.moveTo["x"]
        toY = move.moveTo["y"]

        for key in self.__cache:
            if isinstance(self.__cache[key], list):
                for idx in range(len(self.__cache[key])):
                    cords = self.__cache[key][idx]
                    if cords["x"] == fromX and cords["y"] == fromY:
                        self.__cache[key][idx]["x"] = toX
                        self.__cache[key][idx]["y"] = toY
            elif (
                    isinstance(self.__cache[key], dict) and
                    self.__cache[key]["x"] == fromX and
                    self.__cache[key]["y"] == fromY
            ):
                self.__cache[key]["x"] = toX
                self.__cache[key]["y"] = toY

    def clearCache(self):
        self.__cache = {self.whitePawn: [], self.whiteKing: None, self.blackPawn: [], self.blackKing: None}

