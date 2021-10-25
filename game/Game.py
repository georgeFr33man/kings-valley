from __future__ import division

import random
from typing import Optional

import game
import ai_algorithms


class Game:
    # Game defaults
    boardWidth = 5
    boardHeight = 5
    moveDirections = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]

    # Players
    whitePlayer = "white"
    blackPlayer = "black"

    # Statistics
    statistics = {
        whitePlayer: {
            "wins": 0,
            "availableMoves": []
        },
        blackPlayer: {
            "wins": 0,
            "availableMoves": []
        },
        "numberOfMoves": []
    }

    def __init__(
            self,
            whitePlayerAi: 'ai_algorithms.AbstractAiAlgorithm' = None,
            blackPlayerAi: 'ai_algorithms.AbstractAiAlgorithm' = None
    ):
        self.board = game.Board.Board(self.boardWidth, self.boardHeight)
        self.whitePlayerAi = whitePlayerAi if whitePlayerAi is not None else None
        self.blackPlayerAi = blackPlayerAi if blackPlayerAi is not None else None

    def play(self) -> None:
        playerTurn = self.whitePlayer
        numberOfMoves = 0

        # Attach board object to AI algorithms
        if self.whitePlayerAi is not None:
            self.whitePlayerAi.setBoard(self.board)
        if self.blackPlayerAi is not None:
            self.blackPlayerAi.setBoard(self.board)

        while self.__whoWon() is None:
            numberOfMoves += 1
            isFirstMove = numberOfMoves <= 2
            availableMoves = game.GameRules.GameRules.getMovesForPlayer(playerTurn, self.board, isFirstMove)

            # AI move selection if available
            if playerTurn == self.whitePlayer and self.whitePlayerAi is not None:
                self.board.move(self.whitePlayerAi.selectMove(availableMoves, playerTurn))
                print("------ Move ------")
                self.board.printBoardState()
            elif playerTurn == self.blackPlayer and self.blackPlayerAi is not None:
                self.board.move(self.blackPlayerAi.selectMove(availableMoves, playerTurn))
            else:
                self.board.move(self.__drawMove(availableMoves))
            playerTurn = self.blackPlayer if playerTurn == self.whitePlayer else self.whitePlayer

            # Statistics
            self.__collectStatistics(playerTurn, availableMoves)

        # Collect end game statistics
        self.statistics[self.__whoWon()]["wins"] += 1
        self.statistics["numberOfMoves"].append(numberOfMoves)

    # Winning rules:
    # King pawn is in the center, or
    # Opponent's king has no available moves
    def __whoWon(self) -> Optional[str]:
        kingsFieldCords = self.board.kingsField
        kingsFieldVal = self.board.getFieldValue(kingsFieldCords["x"], kingsFieldCords["y"])
        if kingsFieldVal == self.board.whiteKing:
            return self.whitePlayer
        if kingsFieldVal == self.board.blackKing:
            return self.blackPlayer

        kingsCords = self.board.getKingsCords()
        whiteKing = kingsCords[self.board.whiteKing]
        blackKing = kingsCords[self.board.blackKing]
        if len(game.GameRules.GameRules.getMoves(whiteKing, self.board, True, False, False)) == 0:
            return self.blackPlayer
        if len(game.GameRules.GameRules.getMoves(blackKing, self.board, True, False, False)) == 0:
            return self.whitePlayer

        return None

    def __getPossibleMove(self, fromX: int, fromY: int, xDir: int = 0, yDir: int = 0) -> dict:
        toX = fromX
        toY = fromY
        while self.board.getFieldValue(toX, toY) == self.board.emptyField or (toY == fromY and toX == fromX):
            toX += xDir
            toY += yDir

        return {
            "toX": toX - xDir,
            "toY": toY - yDir
        }

    def __drawMove(self, moves: list) -> game.Move.Move:
        losing = 0
        random.shuffle(moves)
        for move in moves:
            if move.winning:
                return move
            if move.losing:
                losing += 1

        if len(moves) == losing:
            return moves.pop()

        while True:
            index = random.randrange(0, len(moves) - 1)
            if not moves[index].losing:
                return moves[index]

    def __collectStatistics(self, player: str, moves: list):
        self.statistics[player]["availableMoves"].append(len(moves))

    def printStatistics(self):
        stats = self.statistics
        avgAvailableMovesWhite = sum(stats[self.whitePlayer]["availableMoves"]) / len(
            stats[self.whitePlayer]["availableMoves"])
        avgAvailableMovesBlack = sum(stats[self.blackPlayer]["availableMoves"]) / len(
            stats[self.blackPlayer]["availableMoves"])
        # Remove a lot of highest number of moves because of multiple repetition of withdrawing moves
        numberOfMoves = self.statistics["numberOfMoves"]
        numberOfMoves.sort()
        # print(numberOfMoves)
        avgNumberOfMoves = sum(numberOfMoves) / len(numberOfMoves)
        print("White player:")
        print("  - wins: " + str(stats[self.whitePlayer]["wins"]))
        print("  - avg available moves: " + str(avgAvailableMovesWhite))
        print("\nBlack player:")
        print("  - wins: " + str(stats[self.blackPlayer]["wins"]))
        print("  - avg available moves: " + str(avgAvailableMovesBlack))
        print("Avg number of moves: " + str(avgNumberOfMoves))