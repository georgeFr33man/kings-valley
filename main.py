from tests.ComplexityTest import ComplexityTest
from tests.MinMaxTest import MinMaxTest
from tests.AlphaBetaTest import AlphaBetaTest
from tests.AlphaBetaSortedTest import AlphaBetaSortedTest
from tests.MonteCarloSearchTest import MonteCarloSearchTest
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

    # pnsTest = PnsTest(100, 2, Game.Game.blackPlayer, 0, 100000)
    # pnsTest.run()

    mcsTest = MonteCarloSearchTest(100, 20)
    mcsTest.run()

