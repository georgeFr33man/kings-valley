import copy

from game import Move
from game import Board
from game import GameRules
from game import Game


class Node:
    NODE_WIN = float(100000)
    NODE_LOSE = float(-100000)
    NODE_UNKNOWN = float(0)

    move: 'Move' = None
    board: 'Board' = None
    playerName: str = None
    isOrPlayer: bool = None
    disproof: int = None
    proof: int = None
    value: float = None

    __parent: 'Node' = None
    __children: list = []

    def __init__(self, move: 'Move', board: 'Board', playerName: str, isOrPlayer: bool = True, parent: 'Node' = None):
        self.move = move
        self.board = board
        self.playerName = playerName
        self.isOrPlayer = isOrPlayer
        self.__parent = parent

    def isExpanded(self) -> bool:
        return len(self.__children) != 0

    def isRoot(self) -> bool:
        return self.__parent is None

    def expandNode(self):
        board = copy.deepcopy(self.board)
        board.move(self.move)
        opponent = self.getOpponent()
        children = GameRules.GameRules.getMovesForPlayer(opponent, board, False)
        for child in children:
            self.__children.append(Node(child, board, opponent, self.isOrPlayer is False, self))

    def getOpponent(self) -> str:
        return Game.Game.whitePlayer if self.playerName == Game.Game.blackPlayer else Game.Game.blackPlayer

    def getParent(self) -> 'Node':
        return self.__parent

    def getChildren(self) -> list:
        return self.__children

    def evalGoal(self) -> None:
        if self.move.winning:
            self.value = self.NODE_WIN
        elif self.move.losing:
            self.value = self.NODE_LOSE
        else:
            self.value = self.NODE_UNKNOWN
