from __future__ import division

import random
import time
from collections import Counter
from typing import Optional
import game
import ai_algorithms
from pns import Pns


class Game:
    # Game defaults
    boardWidth: int = 5
    boardHeight: int = 5
    moveDirections: list = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]

    # Players
    whitePlayer: str = "white"
    blackPlayer: str = "black"

    # Statistics
    statistics: dict = {
        whitePlayer: {
            "wins": 0,
            "availableMoves": []
        },
        blackPlayer: {
            "wins": 0,
            "availableMoves": []
        },
        "numberOfMoves": [],
        "timeElapsed": 0,
        "proves": [],
        "disproves": []
    }

    def __init__(
            self,
            whitePlayerAi: 'ai_algorithms.AbstractAiAlgorithm' = None,
            blackPlayerAi: 'ai_algorithms.AbstractAiAlgorithm' = None,
            maxRounds: int = None,
            ourPlayer: str = None,
            resources: float = None
    ):
        self.board = game.Board.Board(self.boardWidth, self.boardHeight)
        self.whitePlayerAi = whitePlayerAi
        self.blackPlayerAi = blackPlayerAi
        self.maxRounds = maxRounds
        self.ourPlayer = ourPlayer
        self.resources = resources

    def play(self) -> None:
        playerTurn = self.whitePlayer
        numberOfMoves = 0

        # Attach board object to AI algorithms
        if self.whitePlayerAi is not None:
            self.whitePlayerAi.setBoard(self.board)
        if self.blackPlayerAi is not None:
            self.blackPlayerAi.setBoard(self.board)

        startTime = time.time()

        while self.__whoWon() is None:
            numberOfMoves += 1
            isFirstMove = numberOfMoves <= 2
            availableMoves = game.GameRules.GameRules.getMovesForPlayer(playerTurn, self.board, isFirstMove)

            # Check if PNS should run now
            runPns = self.maxRounds is not None and int(numberOfMoves / 2) == self.maxRounds

            # AI move selection if available
            if playerTurn == self.whitePlayer and self.whitePlayerAi is not None:
                selectedMove = self.whitePlayerAi.selectMove(availableMoves, playerTurn)
                # Run PNS algorithm and break the game.
                if runPns and self.ourPlayer == self.whitePlayer:
                    pns = Pns(self.resources)
                    self.__collectPnsStats(pns.run(selectedMove, self.board, self.whitePlayer))
                    break

                self.board.move(selectedMove)
            elif playerTurn == self.blackPlayer and self.blackPlayerAi is not None:
                selectedMove = self.blackPlayerAi.selectMove(availableMoves, playerTurn)
                # Run PNS algorithm and break the game.
                if runPns and self.ourPlayer == self.blackPlayer:
                    pns = Pns(self.resources)
                    self.__collectPnsStats(pns.run(selectedMove, self.board, self.blackPlayer))
                    break

                self.board.move(selectedMove)
            else:
                selectedMove = self.__drawMove(availableMoves)
                # Run PNS algorithm and break the game.
                if runPns:
                    pns = Pns(self.resources)
                    self.__collectPnsStats(pns.run(selectedMove, self.board, self.ourPlayer))
                    break

                self.board.move(selectedMove)

            playerTurn = self.blackPlayer if playerTurn == self.whitePlayer else self.whitePlayer

            # Statistics
            self.__collectStatistics(playerTurn, availableMoves)

        endTime = time.time()

        # Collect end game statistics
        if self.maxRounds is None:
            self.statistics[self.__whoWon()]["wins"] += 1
            self.statistics["numberOfMoves"].append(numberOfMoves)
            self.statistics["timeElapsed"] += (endTime - startTime)

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

    def __collectPnsStats(self, statistics: dict):
        self.statistics["proves"].append(statistics["proof"])
        self.statistics["disproves"].append(statistics["disproof"])

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
        print("Time elapsed: " + str(self.statistics["timeElapsed"]))

    def printPnsStatistics(self):
        print("\nProves")
        print(Counter(self.statistics["proves"]))
        print("\nDisproves")
        print(Counter(self.statistics["disproves"]))
