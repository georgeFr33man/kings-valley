from abc import ABC, abstractmethod
import game


class AbstractAiAlgorithm(ABC):

    @abstractmethod
    def selectMove(self, moves: list, player: str) -> 'game.Move.Move':
        ...

    @abstractmethod
    def setBoard(self, board: 'game.Board.Board'):
        ...

    @abstractmethod
    def getBoard(self) -> 'game.Board.Board':
        ...
