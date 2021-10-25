import copy
from abc import ABC
from random import shuffle

import game

from ai_algorithms.AbstractAiAlgorithm import AbstractAiAlgorithm


class MinMax(AbstractAiAlgorithm, ABC):
    # Game state evaluation values
    evaluate_Lose = float(-1000000)
    evaluate_Win = float(1000000)
    evaluate_CanWin = float(500000)
    evaluate_CanLose = float(-500000)
    evaluate_GoodMove = float(250000)
    evaluate_BadMove = float(-250000)
    evaluate_Unknown = float(0)

    def __init__(self, depth: int):
        super().__init__()
        self.depth = depth
        self.board = None

    def setBoard(self, board: 'game.Board.Board'):
        self.board = board

    def getBoard(self) -> 'game.Board.Board':
        return self.board

    def selectMove(self, moves: list, player: str) -> 'game.Move.Move':
        val = self.evaluate_Lose
        selectedMoveIndex = 0
        for index, move in enumerate(moves):
            if move.isKing and (move.isWinning == True):
                print('this should be selected now and game should ended')
                print("Move: " + str(move.moveFrom) + " " + str(move.moveTo))
            evaluation = self.minmax(move, self.depth, False, player, self.board)
            if evaluation > val:
                val = evaluation
                selectedMoveIndex = int(index)

        return moves[selectedMoveIndex]

    def minmax(
            self,
            move: 'game.Move.Move',
            depth: int,
            maximizingPlayer: bool,
            playerName: str,
            board: 'game.Board.Board',
    ) -> float:
        if depth == 0 or self.__isEndMove(move):
            board = copy.deepcopy(board)
            return self.__getMoveEvaluation(move, maximizingPlayer, board)
        if maximizingPlayer:
            board = copy.deepcopy(board)
            playerName = game.Game.Game.whitePlayer if playerName == game.Game.Game.blackPlayer else game.Game.Game.blackPlayer
            children = self.__getMoveChildrenMoves(move, playerName, board)
            value = self.evaluate_Lose
            for child in children:
                value = max(value, self.minmax(child, depth - 1, False, playerName, board))
            return value
        else:
            board = copy.deepcopy(board)
            playerName = game.Game.Game.blackPlayer if playerName == game.Game.Game.whitePlayer else game.Game.Game.whitePlayer
            children = self.__getMoveChildrenMoves(move, playerName, board)
            value = self.evaluate_Win
            for child in children:
                value = min(value, self.minmax(child, depth - 1, True, playerName, board))
            return value

    def __isEndMove(self, move: 'game.Move.Move') -> bool:
        return move.losing or move.winning

    def __getMoveEvaluation(self, move: 'game.Move.Move', maximizingPlayer: bool, board: 'game.Board.Board') -> float:
        if move.winning:
            return self.evaluate_Win if maximizingPlayer is False else self.evaluate_Lose

        if move.losing:
            return self.evaluate_Lose if maximizingPlayer is False else self.evaluate_Win

        if move.isGivingOpportunityToLose(board):
            return self.evaluate_Lose if maximizingPlayer is False else self.evaluate_Win

        if move.isGivingOpportunityToWin(board):
            return self.evaluate_Win if maximizingPlayer is False else self.evaluate_Lose

        if move.isFoilingOpponentWinning(board) or move.isFreeingPlayerKing(board):
            return self.evaluate_GoodMove if maximizingPlayer is False else self.evaluate_BadMove

        if move.isBlockingPlayerKing(board):
            return self.evaluate_CanLose if maximizingPlayer is False else self.evaluate_CanWin

        if move.isBlockingOpponentKing(board):
            return self.evaluate_CanWin if maximizingPlayer is False else self.evaluate_CanLose

        return self.evaluate_Unknown

    def __getMoveChildrenMoves(self, move: 'game.Move.Move', playerName: str, board: 'game.Board.Board') -> list:
        board.move(move)

        return game.GameRules.GameRules.getMovesForPlayer(playerName, board, False)
