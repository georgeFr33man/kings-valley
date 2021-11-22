import copy
from abc import ABC

import game

from ai_algorithms.AbstractAiAlgorithm import AbstractAiAlgorithm


class AlphaBetaSorted(AbstractAiAlgorithm, ABC):
    # Game state evaluation values
    evaluate_Lose = float(-1000000)
    evaluate_Win = float(1000000)

    evaluate_NearWin = float(900000)
    evaluate_NearLose = float(-900000)

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
        moves = self.__sortChildren(moves, True, self.board)

        for index, move in enumerate(moves):
            if move.winning:  # speed up the process a little bit.
                return move
            evaluation = self.alphaBeta(move, self.depth, False, player, self.board)
            if evaluation > val:
                val = evaluation
                selectedMoveIndex = int(index)

        return moves[selectedMoveIndex]

    def alphaBeta(
            self,
            move: 'game.Move.Move',
            depth: int,
            maximizingPlayer: bool,
            playerName: str,
            board: 'game.Board.Board',
            alpha: float = -1000000.0,
            beta: float = 1000000.0,
    ) -> float:
        if depth == 0 or self.__isEndMove(move):
            board = copy.deepcopy(board)
            return self.__getMoveEvaluation(move, maximizingPlayer, board)
        if maximizingPlayer:
            board = copy.deepcopy(board)
            playerName = game.Game.Game.whitePlayer \
                if playerName == game.Game.Game.blackPlayer \
                else game.Game.Game.blackPlayer
            children = self.__sortChildren(
                self.__getMoveChildrenMoves(move, playerName, board), maximizingPlayer, board
            )
            for child in children:
                alpha = max(alpha, self.alphaBeta(child, depth - 1, False, playerName, board, alpha, beta))
                if alpha >= beta:
                    return beta
            return alpha
        else:
            board = copy.deepcopy(board)
            playerName = game.Game.Game.blackPlayer \
                if playerName == game.Game.Game.whitePlayer \
                else game.Game.Game.whitePlayer
            children = self.__sortChildren(
                self.__getMoveChildrenMoves(move, playerName, board), maximizingPlayer, board
            )
            for child in children:
                beta = min(beta, self.alphaBeta(child, depth - 1, True, playerName, board, alpha, beta))
                if alpha >= beta:
                    return alpha
            return beta

    def __isEndMove(self, move: 'game.Move.Move') -> bool:
        return move.losing or move.winning

    def __getMoveEvaluation(self, move: 'game.Move.Move', maximizingPlayer: bool, board: 'game.Board.Board') -> float:
        if move.winning:
            return self.evaluate_Win if maximizingPlayer is False else self.evaluate_Lose

        if move.losing:
            return self.evaluate_Lose if maximizingPlayer is False else self.evaluate_Win

        if move.isGivingOpportunityToLose(board):
            return self.evaluate_NearLose if maximizingPlayer is False else self.evaluate_NearWin

        if move.isGivingOpportunityToWin(board):
            return self.evaluate_NearWin if maximizingPlayer is False else self.evaluate_NearLose

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

    def __sortChildren(
            self,
            children: list,
            maximizingPlayer: bool,
            board: 'game.Board.Board'
    ) -> list:
        childrenValues = []
        sortedChildren = []
        for index, childMove in enumerate(children):
            childrenValues.append(
                {'index': index, 'value': self.__getMoveEvaluation(childMove, maximizingPlayer, board)}
            )

        if maximizingPlayer:
            sortedChildrenList = sorted(childrenValues, key=lambda i: i['value'], reverse=True)
        else:
            sortedChildrenList = sorted(childrenValues, key=lambda i: i['value'])

        for sortedChild in sortedChildrenList:
            sortedChildren.append(children[sortedChild['index']])

        return sortedChildren
