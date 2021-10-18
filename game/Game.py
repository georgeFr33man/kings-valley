from __future__ import division

import copy
import random
from game.Board import Board


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

    def __init__(self):
        self.board = Board(self.boardWidth, self.boardHeight)

    def play(self):
        playerTurn = self.whitePlayer
        playersMoves = {
            self.whitePlayer: 0,
            self.blackPlayer: 0
        }
        numberOfmoves = 0
        while self.__whoWon() is None:
            numberOfmoves += 1
            if playerTurn == self.whitePlayer and playersMoves[playerTurn] == 0:
                isFirstMove = True
            elif playerTurn == self.blackPlayer and playersMoves[playerTurn] == 0:
                isFirstMove = True
            else:
                isFirstMove = False
            moves = self.__getAllAvailableMoves(playerTurn, isFirstMove)
            self.__move(self.__drawMove(moves))
            playersMoves[playerTurn] = playersMoves[playerTurn] + 1
            playerTurn = self.blackPlayer if playerTurn == self.whitePlayer else self.whitePlayer
            self.__collectStatistics(playerTurn, moves)

        # Collect end game statistics
        self.statistics[self.__whoWon()]["wins"] += 1
        self.statistics["numberOfMoves"].append(numberOfmoves)

    # Winning rules:
    # King pawn in in the center, or
    # Opponent's king has no available moves
    def __whoWon(self):
        kingsFieldCords = self.board.getKingsValleyFieldCords()
        kingsFieldVal = self.board.getFieldValue(kingsFieldCords["x"], kingsFieldCords["y"])
        if kingsFieldVal == self.board.whiteKing:
            return self.whitePlayer
        if kingsFieldVal == self.board.blackKing:
            return self.blackPlayer

        kingsCords = self.board.getKingsCords()
        whiteKing = kingsCords["whiteKing"]
        blackKing = kingsCords["blackKing"]
        if len(self.__getMoves(whiteKing["x"], whiteKing["y"], True, False)) == 0:
            return self.blackPlayer
        if len(self.__getMoves(blackKing["x"], blackKing["y"], True, False)) == 0:
            return self.whitePlayer

        return None

    def __getAllAvailableMoves(self, player, isFirstMove=False):
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
                        getMoves = self.__getMoves(x, y, False, isFirstMove, player)
                        if len(getMoves) > 0:
                            moves.extend(getMoves)
                    elif fieldVal == acceptableValues[1]:
                        getMoves = self.__getMoves(x, y, True, isFirstMove, player)
                        if len(getMoves) > 0:
                            moves.extend(getMoves)

        return moves

    def __getMoves(self, x, y, isKing, isFistMove, player=None):
        moves = []
        directions = copy.copy(self.moveDirections)
        random.shuffle(directions)
        for direction in directions:
            possibleMove = self.__getPossibleMove(x, y, direction[0], direction[1])
            toX = possibleMove["toX"]
            toY = possibleMove["toY"]
            if self.__canBeMoved(x, y, toX, toY, isKing, isFistMove):
                move = self.__createMove(x, y, toX, toY)
                move = self.__checkMove(move, isKing, isFistMove, player)
                moves.append(move)

        return moves

    def __getPossibleMove(self, fromX, fromY, xDir=0, yDir=0):
        toX = fromX
        toY = fromY
        while self.board.getFieldValue(toX, toY) == self.board.emptyField or (toY == fromY and toX == fromX):
            toX += xDir
            toY += yDir

        return {
            "toX": toX - xDir,
            "toY": toY - yDir
        }

    def __canBeMoved(self, fromX, fromY, toX, toY, isKing, isFistMove):
        kingsValley = self.board.getKingsValleyFieldCords()
        if isKing and isFistMove:
            return False
        if fromX == toX and fromY == toY:
            return False
        if kingsValley["x"] == toX and kingsValley["y"] == toY and isKing == False:
            return False

        return True

    def __createMove(self, fromX, fromY, toX, toY):
        return {
            "from": {"x": fromX, "y": fromY},
            "to": {"x": toX, "y": toY},
            "winning": False,
            "winningByKing": False,
            "losing": False
        }

    def __checkMove(self, move, isKing, isFistMove, player=None):
        if isFistMove:
            return move
        kingsValley = self.board.getKingsValleyFieldCords()

        if isKing and move["to"]["x"] == kingsValley["x"] and move["to"]["y"] == kingsValley["y"]:
            move["winningByKing"] = True

        if player is not None:
            kingsCords = self.board.getKingsCords()
            opponentKing = kingsCords["blackKing"] if player == self.whitePlayer else kingsCords["whiteKing"]
            playerKing = kingsCords["whiteKing"] if player == self.whitePlayer else kingsCords["blackKing"]
            opponentKingMoves = self.__getMoves(opponentKing["x"], opponentKing["y"], False, True)
            playerKingMoves = self.__getMoves(playerKing["x"], playerKing["y"], False, True)

            if len(opponentKingMoves) <= 1:
                if (
                    self.__isMoveNextToField(
                        move["from"]["x"],
                        move["from"]["y"],
                        opponentKing["x"],
                        opponentKing["y"]
                    ) is False and
                    self.__isMoveNextToField(move["to"]["x"], move["to"]["y"], opponentKing["x"], opponentKing["y"])
                ):
                    move["winning"] = True
            if len(playerKingMoves) <= 1 and isKing is False:
                if self.__isMoveNextToField(move["to"]["x"], move["to"]["y"], playerKing["x"], playerKing["y"]):
                    move["losing"] = True

        return move

    def __isMoveNextToField(self, moveX, moveY, fieldX, fieldY):
        for direction in self.moveDirections:
            if moveX + direction[0] == fieldX and moveY + direction[1] == fieldY:
                return True

        return False

    def __move(self, move):
        fieldValue = self.board.getFieldValue(move["from"]["x"], move["from"]["y"])
        self.board.setFieldValue(move["from"]["x"], move["from"]["y"], self.board.emptyField)
        self.board.setFieldValue(move["to"]["x"], move["to"]["y"], fieldValue)

    def __drawMove(self, moves):
        losing = 0
        random.shuffle(moves)
        for move in moves:
            if move["winningByKing"]:
                return move
            if move["winning"]:
                return move
            if move["losing"]:
                losing += 1

        if len(moves) == losing:
            return moves.pop()

        while True:
            index = random.randrange(0, len(moves) - 1)
            if not moves[index]["losing"]:
                return moves[index]

    def __collectStatistics(self, player, moves):
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
        print ("  - wins: " + str(stats[self.whitePlayer]["wins"]))
        print ("  - avg available moves: " + str(avgAvailableMovesWhite))
        print("\nBlack player:")
        print ("  - wins: " + str(stats[self.blackPlayer]["wins"]))
        print ("  - avg available moves: " + str(avgAvailableMovesBlack))
        print("Avg number of moves: " + str(avgNumberOfMoves))
