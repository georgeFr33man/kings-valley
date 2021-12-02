from __future__ import division
import game as g
from ai_algorithms import AlphaBetaSorted


class PnsTest:
    def __init__(self, testCases: int, maxMoves: int, playerName: str, absDepth: int, resources: float):
        self.__testCases: int = testCases
        self.__depth = absDepth
        self.__maxMoves = maxMoves
        self.__playerName = playerName
        self.__resources = resources

    def run(self):
        # 1. Play game with AlphaBetaSorted algorithms.
        # Stop after given number of moves and try to proof win/lose of the selected player
        print("Running PNS algorithm tests on " + str(self.__testCases) + " tests cases.")
        abs1 = AlphaBetaSorted(self.__depth)
        # abs2 = AlphaBetaSorted(self.__depth - 1)
        game = g.Game.Game(abs1, None, self.__maxMoves, self.__playerName, self.__resources)
        for i in range(self.__testCases):
            print("Playing: " + str(i + 1) + " game.")
            game.board.restoreStarterBoard()
            game.play()
