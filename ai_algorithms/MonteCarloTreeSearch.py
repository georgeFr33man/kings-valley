import copy

import numpy as np

from abc import ABC
import game

from ai_algorithms.AbstractAiAlgorithm import AbstractAiAlgorithm


class MonteCarloTreeSearch(AbstractAiAlgorithm, ABC):

    def __init__(self, depth: int):
        super().__init__()
        self.depth = depth
        self.board = None

    def setBoard(self, board: 'game.Board.Board'):
        self.board = board

    def getBoard(self) -> 'game.Board.Board':
        return self.board

    def selectMove(self, moves: list, player: str) -> 'game.Move.Move':
        return self.monteCarloSearch(moves, player, self.board)

    def monteCarloSearch(
            self,
            moves: list,
            playerName: str,
            board: 'game.Board.Board',
    ) -> 'game.Move.Move':
        root = Node(board, playerName, None, None, moves)
        root.playerName = root.getOpponent()

        for i in range(self.depth):
            current = Node.treePolicy(root)
            reward = Node.defaultPolicy(current)
            Node.backUp(current, reward)

        return Node.bestChild(root).move


class Node:
    move: 'Move' = None
    board: 'Board' = None
    playerName: str = None
    results = {
        'win': 0,
        'lose': 0
    }
    children: list = []

    __numberOfVisits: int = 0
    __parent: 'Node' = None
    __untriedActions: list = []

    def __init__(
            self,
            board: 'Board',
            playerName: str,
            move: 'Move' = None,
            parent: 'Node' = None,
            moves: list = None
    ):
        self.move = move
        self.board = board
        self.playerName = playerName
        self.__parent = parent
        self.untriedActions(moves)

    def getOpponent(self) -> str:
        return game.Game.Game.whitePlayer if self.playerName == game.Game.Game.blackPlayer else game.Game.Game.blackPlayer

    def getParent(self) -> 'Node':
        return self.__parent

    def untriedActions(self, actions: list = None):
        board = copy.deepcopy(self.board)

        if actions is None:
            board.move(self.move)
            opponent = self.getOpponent()
            actions = game.GameRules.GameRules.getMovesForPlayer(opponent, board, False)

        for action in actions:
            self.__untriedActions.append(action)

    def isFullyExpanded(self):
        return len(self.__untriedActions) == 0

    def isTerminalNode(self):
        if self.move is None:
            return False

        return self.move.losing or self.move.winning

    def v(self):
        return self.results['win'] - self.results['lose']

    def n(self):
        return self.__numberOfVisits

    def nIncrease(self):
        self.__numberOfVisits = self.__numberOfVisits + 1

    @classmethod
    def expand(cls, node: 'Node'):
        child = Node(node.board, node.getOpponent(), node.__untriedActions.pop(), node)
        node.children.append(child)

        return child

    @classmethod
    def treePolicy(cls, node: 'Node') -> 'Node':
        while node.isTerminalNode() is False:
            if node.isFullyExpanded() is False:
                return Node.expand(node)
            else:
                node = Node.bestChild(node)

        return node

    @classmethod
    def bestChild(cls, node: 'Node', cParam = 0.1) -> 'Node':
        choicesWeights = [
            (child.v() / child.n()) + cParam * np.sqrt((2 * np.log(node.n()) / child.n())) for child in node.children
        ]

        return node.children[np.argmax(choicesWeights)]

    @classmethod
    def defaultPolicy(cls, node: 'Node') -> str:
        boardCopy = copy.deepcopy(node.board)
        current = node
        opponent = game.GameRules.GameRules.getOpponent(current.playerName)
        while current.isTerminalNode() is False:
            boardCopy.move(current.move)
            childMoves = game.GameRules.GameRules.getMovesForPlayer(opponent, boardCopy, False)
            current = Node(boardCopy, opponent, game.Game.Game.drawMove(childMoves))
            opponent = game.GameRules.GameRules.getOpponent(opponent)

        return 'win' if current.playerName == node.playerName and current.move.winning else 'lose'

    @classmethod
    def backUp(cls, node: 'Node', reward: str):
        while node is not None:
            node.nIncrease()
            node.results[reward] += 1
            node = node.getParent()

