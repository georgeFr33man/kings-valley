from tests.ComplexityTest import ComplexityTest
from tests.MinMaxTest import MinMaxTest
from tests.AlphaBetaTest import AlphaBetaTest
from tests.AlphaBetaSortedTest import AlphaBetaSortedTest

if __name__ == '__main__':
    # complexityTest = ComplexityTest(1000)
    # complexityTest.run()

    minMaxTest = MinMaxTest(10, 5)
    minMaxTest.run()

    minMaxTest = MinMaxTest(10, 6)
    minMaxTest.run()

    alphaBetaTest = AlphaBetaTest(10, 5)
    alphaBetaTest.run()

    # alphaBetaSortedTest = AlphaBetaSortedTest(1, 10)
    # alphaBetaSortedTest.run()


