from __future__ import division
import random

import game as g


class ComplexityTest:
    def __init__(self, testCases: int):
        self.__testCases: int = testCases
        self.boardWidth: int = 5
        self.boardHeight: int = 5

    def run(self):
        # 1. Generate random boards
        print("Running generating tests on " + str(self.__testCases) + " tests cases.")
        valid = 0
        for i in range(self.__testCases):
            randomBoard = self.createRandomBoardState()
            valid += 1 if self.validateBoardState(randomBoard) else 0

        # 2. Play game randomly
        print("Running playing tests on " + str(self.__testCases) + " tests cases.")
        game = g.Game.Game()
        for i in range(self.__testCases):
            print("Playing: " + str(i + 1) + " game.")
            game.board.restoreStarterBoard()
            game.play()

        game.printStatistics()
        print("Valid: " + str(valid) + " out of: " + str(self.__testCases) + " (" + str(
            float(valid / self.__testCases)) + ")")

    def createRandomBoardState(self) -> g.Board.Board:
        board = g.Board.Board(self.boardWidth, self.boardHeight)
        emptyElementsCount = (self.boardWidth * self.boardHeight) - (2 * self.boardWidth)

        # Add empty elements.
        availableElements = [board.emptyField for i in range(emptyElementsCount)]
        # Add white pawn elements.
        availableElements.extend(board.whitePawn for i in range(self.boardWidth - 1))
        # Add black pawn elements.
        availableElements.extend(board.blackPawn for i in range(self.boardWidth - 1))
        # Add kings elements.
        availableElements.extend([board.blackKing, board.whiteKing])

        # Insert one element foreach field on the board.
        for y in range(board.boardHeight):
            for x in range(board.boardWidth):
                elementsLen = len(availableElements)
                if elementsLen == 1:
                    board.setFieldValue(x, y, availableElements.pop())
                else:
                    drawIndex = random.randrange(-1, elementsLen - 1)
                    board.setFieldValue(x, y, availableElements.pop(drawIndex))

        return board

    @staticmethod
    def validateBoardState(board: g.Board.Board) -> bool:
        # Rules:
        # 1. Only the king can stand in the middle of the board.
        kingsValley = board.kingsField
        kingsValleyVal = board.getFieldValue(kingsValley["x"], kingsValley["y"])

        return kingsValleyVal != board.blackPawn and kingsValleyVal != board.whitePawn
