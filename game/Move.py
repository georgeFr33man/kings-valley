import copy

import game as g


class Move:
    def __init__(self, fromCords: dict, toCords: dict, moveDirections: list, isKing: bool, isFirstMove: bool):
        self.moveFrom = {"x": fromCords["x"], "y": fromCords["y"]}
        self.moveTo = {"x": toCords["x"], "y": toCords["y"]}
        self.isKing = isKing
        self.isFirstMove = isFirstMove
        self.winning = False
        self.losing = False
        self.moveDirections = moveDirections

    def getMovePieceValue(self, board):
        return board.getFieldValue(self.moveFrom["x"], self.moveFrom["y"])

    def getOpponentKing(self, board: 'g.Board.Board'):
        kingsCords = board.getKingsCords()
        movePieceValue = self.getMovePieceValue(board)

        return kingsCords[board.blackKing] if movePieceValue in [board.whiteKing, board.whitePawn] else kingsCords[
            board.whiteKing]

    def getPlayerKing(self, board: 'g.Board.Board'):
        kingsCords = board.getKingsCords()
        movePieceValue = self.getMovePieceValue(board)

        return kingsCords[board.whiteKing] if movePieceValue in [board.whiteKing, board.whitePawn] else kingsCords[
            board.blackKing]

    def checkMoveProperties(self, board: 'g.Board.Board') -> None:
        if self.isFirstMove:
            return None
        self.winning = self.isWinning(board)
        self.losing = self.isLosing(board)

    def isWinning(self, board: 'g.Board.Board') -> bool:
        kingsValley = board.kingsField
        if self.isKing and self.moveTo["x"] == kingsValley["x"] and self.moveTo["y"] == kingsValley["y"]:
            return True

        opponentKing = self.getOpponentKing(board)
        opponentKingMoves = g.GameRules.GameRules.getMoves(opponentKing, board, True, False, False)
        if len(opponentKingMoves) <= 1:
            return (
                    self.__isNextToField(opponentKing) is False and
                    self.__isMoveNextToField(opponentKing)
            )

    def isLosing(self, board: 'g.Board.Board') -> bool:
        playerKing = self.getPlayerKing(board)
        playerKingMoves = g.GameRules.GameRules.getMoves(playerKing, board, True, False, False)
        if len(playerKingMoves) <= 1 and self.isKing is False:
            return self.__isMoveNextToField(playerKing)

    def isGivingOpportunityToLose(self, board: 'g.Board.Board') -> bool:
        opponentKing = self.getOpponentKing(board)
        board = copy.deepcopy(board)
        board.move(self)
        opponentKingMoves = g.GameRules.GameRules.getMoves(opponentKing, board, True, False, False)
        kingsValley = board.kingsField

        for opponentKingMove in opponentKingMoves:
            if opponentKingMove.moveTo["x"] == kingsValley["x"] and opponentKingMove.moveTo["y"] == kingsValley["y"]:
                return True

        return False

    def isGivingOpportunityToWin(self, board: 'g.Board.Board') -> bool:
        playerKing = self.getPlayerKing(board)
        board = copy.deepcopy(board)
        board.move(self)
        playerKingMoves = g.GameRules.GameRules.getMoves(playerKing, board, True, False, False)
        kingsValley = board.kingsField

        for playerKingMove in playerKingMoves:
            if playerKingMove.moveTo["x"] == kingsValley["x"] and playerKingMove.moveTo["y"] == kingsValley["y"]:
                return True

        return False

    def isFoilingOpponentWinning(self, board: 'g.Board.Board') -> bool:
        opponentKing = self.getOpponentKing(board)
        kingsValley = board.kingsField
        board = copy.deepcopy(board)
        opponentKingCanWin = False
        opponentKingMoves = g.GameRules.GameRules.getMoves(opponentKing, board, True, False, False)
        for opponentKingMove in opponentKingMoves:
            if opponentKingMove.moveTo["x"] == kingsValley["x"] and opponentKingMove.moveTo["y"] == kingsValley["y"]:
                opponentKingCanWin = True
        if opponentKingCanWin is False:
            return False
        board.move(self)
        opponentKingCanWin = False
        opponentKingMoves = g.GameRules.GameRules.getMoves(opponentKing, board, True, False, False)
        for opponentKingMove in opponentKingMoves:
            if opponentKingMove.moveTo["x"] == kingsValley["x"] and opponentKingMove.moveTo["y"] == kingsValley["y"]:
                return False

        return True

    def isFreeingPlayerKing(self, board: 'g.Board.Board') -> bool:
        playerKing = self.getPlayerKing(board)
        return self.__isNextToField(playerKing)

    def isBlockingOpponentKing(self, board: 'g.Board.Board') -> bool:
        opponentKing = self.getOpponentKing(board)
        return self.__isMoveNextToField(opponentKing)

    def isBlockingPlayerKing(self, board: 'g.Board.Board') -> bool:
        playerKing = self.getPlayerKing(board)
        return self.__isMoveNextToField(playerKing)


    def __isMoveNextToField(self, cords: dict) -> bool:
        for direction in self.moveDirections:
            if self.moveTo["x"] + direction[0] == cords["x"] and self.moveTo["y"] + direction[1] == cords["y"]:
                return True

        return False

    def __isNextToField(self, cords: dict) -> bool:
        for direction in self.moveDirections:
            if self.moveFrom["x"] + direction[0] == cords["x"] and self.moveFrom["y"] + direction[1] == cords["y"]:
                return True

        return False
