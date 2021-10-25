from __future__ import division

import game as g
from ai_algorithms import MinMax


class MinMaxTest:
    def __init__(self, testCases: int, depth: int):
        self.__testCases: int = testCases
        self.__depth = depth
        self.boardWidth: int = 5
        self.boardHeight: int = 5

    def run(self):
        # 1. Play game with min max algorithm
        print("Running min max playing tests on " + str(self.__testCases) + " tests cases.")
        minMax = MinMax(self.__depth)
        minMax2 = MinMax(self.__depth + 1)
        game = g.Game.Game(minMax, minMax2)
        for i in range(self.__testCases):
            print("Playing: " + str(i + 1) + " game.")
            game.board.restoreStarterBoard()
            game.play()

        game.printStatistics()
