from __future__ import division

import copy
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
            whitePlayerAi: 'ai_algorithms.AiAlgorithmInterface' = None,
            blackPlayerAi: 'ai_algorithms.AiAlgorithmInterface' = None
    ):
        self.board = game.Board.Board(self.boardWidth, self.boardHeight)
        self.whitePlayerAi = whitePlayerAi(self.board) if whitePlayerAi is not None else None
        self.blackPlayerAi = blackPlayerAi(self.board) if blackPlayerAi is not None else None

    def play(self) -> None:
        playerTurn = self.whitePlayer
        numberOfMoves = 0
        while self.__whoWon() is None:
            numberOfMoves += 1
            isFirstMove = numberOfMoves <= 2
            availableMoves = self.__getAllAvailableMoves(playerTurn, isFirstMove)

            # AI move selection if available
            if playerTurn == self.whitePlayer and self.whitePlayerAi is not None:
                self.__move(self.whitePlayerAi.selectMove(availableMoves))
            elif playerTurn == self.blackPlayerAi and self.blackPlayerAi is not None:
                self.__move(self.blackPlayerAi.selectMove(availableMoves))
            else:
                self.__move(self.__drawMove(availableMoves))
            playerTurn = self.blackPlayer if playerTurn == self.whitePlayer else self.whitePlayer

            # Statistics
            self.__collectStatistics(playerTurn, availableMoves)

        # Collect end game statistics
        self.statistics[self.__whoWon()]["wins"] += 1
        self.statistics["numberOfMoves"].append(numberOfMoves)

    # Winning rules:
    # King pawn in in the center, or
    # Opponent's king has no available moves
    def __whoWon(self) -> Optional[str]:
        kingsFieldCords = self.board.getKingsValleyFieldCords()
        kingsFieldVal = self.board.getFieldValue(kingsFieldCords["x"], kingsFieldCords["y"])
        if kingsFieldVal == self.board.whiteKing:
            return self.whitePlayer
        if kingsFieldVal == self.board.blackKing:
            return self.blackPlayer

        kingsCords = self.board.getKingsCords()
        whiteKing = kingsCords["whiteKing"]
        blackKing = kingsCords["blackKing"]
        if len(self.getMoves(whiteKing["x"], whiteKing["y"], True, False)) == 0:
            return self.blackPlayer
        if len(self.getMoves(blackKing["x"], blackKing["y"], True, False)) == 0:
            return self.whitePlayer

        return None

    def __getAllAvailableMoves(self, player: str, isFirstMove: bool = False) -> list:
        # Move rules:
        # 1. First move must be a pawn move.
        # 2. You can move in any direction but always as far as possible.
        # 3. You have to move.
        # 4. Pawn cannot move to the center.
        moves = []
        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                fieldVal = self.board.getFieldValue(x, y)
                if fieldVal != self.board.emptyField:
                    acceptableValues = []
                    if player == self.whitePlayer:
                        acceptableValues = [self.board.whitePawn, self.board.whiteKing]
                    elif player == self.blackPlayer:
                        acceptableValues = [self.board.blackPawn, self.board.blackKing]
                    if fieldVal == acceptableValues[0]:
                        getMoves = self.getMoves(x, y, False, isFirstMove, player)
                        if len(getMoves) > 0:
                            moves.extend(getMoves)
                    elif fieldVal == acceptableValues[1]:
                        getMoves = self.getMoves(x, y, True, isFirstMove, player)
                        if len(getMoves) > 0:
                            moves.extend(getMoves)

        return moves

    def getMoves(self, x: int, y: int, isKing: bool, isFistMove: bool, player: str = None) -> list:
        moves = []
        directions = copy.copy(self.moveDirections)
        random.shuffle(directions)
        for direction in directions:
            possibleMove = self.__getPossibleMove(x, y, direction[0], direction[1])
            toX = possibleMove["toX"]
            toY = possibleMove["toY"]
            if self.__canBeMoved(x, y, toX, toY, isKing, isFistMove):
                move = game.Move.Move(x, y, toX, toY, self.moveDirections)
                move.checkMoveInGame(self, isKing, isFistMove, player)
                moves.append(move)

        return moves

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

    def __canBeMoved(self, fromX: int, fromY: int, toX: int, toY: int, isKing: bool, isFistMove: bool) -> bool:
        kingsValley = self.board.getKingsValleyFieldCords()
        if isKing and isFistMove:
            return False
        if fromX == toX and fromY == toY:
            return False
        if kingsValley["x"] == toX and kingsValley["y"] == toY and isKing is False:
            return False

        return True

    def __move(self, move: game.Move.Move):
        fieldValue = self.board.getFieldValue(move.moveFrom["x"], move.moveFrom["y"])
        self.board.setFieldValue(move.moveFrom["x"], move.moveFrom["y"], self.board.emptyField)
        self.board.setFieldValue(move.moveTo["x"], move.moveTo["y"], fieldValue)

    def __drawMove(self, moves: list) -> game.Move.Move:
        losing = 0
        random.shuffle(moves)
        for move in moves:
            if move.winningByKing:
                return move
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