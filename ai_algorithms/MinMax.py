from abc import ABC
import game

from ai_algorithms.AbstractAiAlgorithm import AbstractAiAlgorithm


class MinMax(AbstractAiAlgorithm, ABC):
    def __init__(self, depth: int):
        super().__init__()
        self.depth = depth
        self.board = None

    def selectMove(self, moves: list, player: str) -> 'game.Move.Move':
        pass

    def setBoard(self, board: 'game.Board.Board'):
        self.board = board

    def getBoard(self) -> 'game.Board.Board':
        return self.board
