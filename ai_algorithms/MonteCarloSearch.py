import copy
import random
import secrets
from abc import ABC
from time import time, time_ns

import game

from ai_algorithms.AbstractAiAlgorithm import AbstractAiAlgorithm


class MonteCarloSearch(AbstractAiAlgorithm, ABC):

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
        bestMove = None
        bestProbability = -1

        for move in moves:
            r = 0
            for x in range(0, self.depth):
                moveCopy = copy.deepcopy(move)
                boardCopy = copy.deepcopy(board)
                opponent = game.GameRules.GameRules.getOpponent(playerName)
                while self.__isEndMove(moveCopy) is False:
                    childMoves = self.__getMoveChildrenMoves(moveCopy, opponent, boardCopy)
                    opponent = game.GameRules.GameRules.getOpponent(opponent)
                    moveCopy = game.Game.Game.drawMove(childMoves)

                if moveCopy.winning is True and opponent != playerName:
                    r += 1
            probability = r / self.depth
            if probability > bestProbability:
                bestMove = move
                bestProbability = probability

        return bestMove

    def __isEndMove(self, move: 'game.Move.Move') -> bool:
        return move.losing or move.winning

    def __getMoveChildrenMoves(self, move: 'game.Move.Move', playerName: str, board: 'game.Board.Board') -> list:
        board.move(move)

        return game.GameRules.GameRules.getMovesForPlayer(playerName, board, False)