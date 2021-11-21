from __future__ import division
import game as g
from ai_algorithms import AlphaBetaSorted


class AlphaBetaSortedTest:
    def __init__(self, testCases: int, depth: int):
        self.__testCases: int = testCases
        self.__depth = depth

    def run(self):
        # 1. Play game with alpha beta algorithm
        print("Running alpha beta sorted playing tests on " + str(self.__testCases) + " tests cases.")
        alphaBeta = AlphaBetaSorted(self.__depth)
        game = g.Game.Game(alphaBeta)
        for i in range(self.__testCases):
            print("Playing: " + str(i + 1) + " game.")
            game.board.restoreStarterBoard()
            game.play()

        game.printStatistics()
