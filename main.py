from tests.ComplexityTest import ComplexityTest
from tests.MinMaxTest import MinMaxTest
from tests.AlphaBetaTest import AlphaBetaTest
from tests.AlphaBetaSortedTest import AlphaBetaSortedTest
from tests.PnsTest import PnsTest
from game import Game


if __name__ == '__main__':
    # complexityTest = ComplexityTest(1000)
    # complexityTest.run()

    # minMaxTest = MinMaxTest(100, 4)
    # minMaxTest.run()

    # minMaxTest = MinMaxTest(100, 4)
    # minMaxTest.run()

    # alphaBetaSortedTest = AlphaBetaSortedTest(2, 4)
    # alphaBetaSortedTest.run()

    # 100 game, max 2 pre-moves, white player, ABS depth = 0 (play random), 10 milliseconds.
    pnsTest = PnsTest(1000, 10, Game.Game.whitePlayer, 0, 1000000)
    pnsTest.run()
