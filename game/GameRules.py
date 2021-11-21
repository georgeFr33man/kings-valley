import game


class GameRules:
    moveDirections: list = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]

    @classmethod
    def getPlayerPawnValue(cls, player: str):
        return game.Board.Board.whitePawn if player == game.Game.Game.whitePlayer else game.Board.Board.blackPawn

    @classmethod
    def getPlayerKingValue(cls, player: str):
        return game.Board.Board.whiteKing if player == game.Game.Game.whitePlayer else game.Board.Board.blackKing

    @classmethod
    def getMovesForPlayer(cls, player: str, board: 'game.Board.Board', isFirstMove: bool = False) -> list:
        # Move rules:
        # 1. First move must be a pawn move.
        # 2. You can move in any direction but always as far as possible.
        # 3. You have to move.
        # 4. Pawn cannot move to the center.
        moves = []
        playerPawns = board.getCache()[cls.getPlayerPawnValue(player)]
        playerKing = board.getCache()[cls.getPlayerKingValue(player)]

        kingMoves = cls.getMoves(playerKing, board, True, isFirstMove)
        if len(kingMoves) > 0:
            moves.extend(kingMoves)

        for pawn in playerPawns:
            pawnMoves = cls.getMoves(pawn, board, False, isFirstMove)
            if len(pawnMoves) > 0:
                moves.extend(pawnMoves)

        return moves

    @classmethod
    def getMoves(
            cls,
            cords: dict,
            board: 'game.Board.Board',
            isKing: bool,
            isFistMove: bool,
            checkForProperties: bool = True
    ) -> list:
        moves = []
        for direction in cls.moveDirections:
            possibleMove = cls.getPossibleMove(cords, direction, board)
            if cls.canBeMoved(cords, possibleMove, board, isKing, isFistMove):
                move = game.Move.Move(cords, possibleMove, cls.moveDirections, isKing, isFistMove)
                if checkForProperties:
                    move.checkMoveProperties(board)
                moves.append(move)

        return moves

    @classmethod
    def getPossibleMove(cls, cords: dict, direction: list, board: 'game.Board.Board') -> dict:
        toX = cords["x"]
        toY = cords["y"]
        while board.getFieldValue(toX, toY) == board.emptyField or (toY == cords["y"] and toX == cords["x"]):
            toX += direction[0]
            toY += direction[1]

        return {
            "x": toX - direction[0],
            "y": toY - direction[1]
        }

    @classmethod
    def canBeMoved(
            cls,
            fromCords: dict,
            toCords: dict,
            board: 'game.Board.Board',
            isKing: bool,
            isFistMove: bool
    ) -> bool:
        kingsValley = board.kingsField
        if isKing and isFistMove:
            return False
        if fromCords["x"] == toCords["x"] and fromCords["y"] == toCords["y"]:
            return False
        if kingsValley["x"] == toCords["x"] and kingsValley["y"] == toCords["y"] and isKing is False:
            return False

        return True
