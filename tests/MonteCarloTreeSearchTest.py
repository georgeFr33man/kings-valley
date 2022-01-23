from __future__ import division
import game as g
from ai_algorithms import MonteCarloTreeSearch


class MonteCarloTreeSearchTest:
    def __init__(self, testCases: int, depth: int):
        self.__testCases: int = testCases
        self.__depth = depth

    def run(self):
        # 1. Play game with monte carlo tree search algorithm
        print("Running monte carlo tree tests on " + str(self.__testCases) + " tests cases with " + str(self.__depth) + " simulations.")
        mcs = MonteCarloTreeSearch(self.__depth)
        game = g.Game.Game(mcs)
        for i in range(self.__testCases):
            print("Playing: " + str(i + 1) + " game.")
            game.board.restoreStarterBoard()
            game.play()

        game.printStatistics()
