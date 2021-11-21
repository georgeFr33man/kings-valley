from __future__ import division
import game as g
from ai_algorithms import AlphaBeta


class AlphaBetaTest:
    def __init__(self, testCases: int, depth: int):
        self.__testCases: int = testCases
        self.__depth = depth

    def run(self):
        # 1. Play game with alpha beta algorithm
        print("Running alpha beta playing tests on " + str(self.__testCases) + " tests cases.")
        alphaBeta = AlphaBeta(self.__depth)
        game = g.Game.Game(alphaBeta)
        for i in range(self.__testCases):
            print("Playing: " + str(i + 1) + " game.")
            game.board.restoreStarterBoard()
            game.play()

        game.printStatistics()
