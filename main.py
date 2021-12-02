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

    # 1 game, max 2 pre-moves, white player, ABS depth = 2, 10 seconds.
    pnsTest = PnsTest(1, 1, Game.Game.whitePlayer, 2, 1)
    pnsTest.run()
