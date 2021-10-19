import game as g

class Move:
    def __init__(self, fromX: int, fromY: int, toX: int, toY: int, moveDirections: list):
        self.moveFrom = {"x": fromX, "y": fromY}
        self.moveTo = {"x": toX, "y": toY}
        self.winning = False
        self.winningByKing = False
        self.losing = False
        self.moveDirections = moveDirections

    def checkMoveInGame(self, game: 'g.Game.Game', isKing: bool, isFirstMove: bool, player: str) -> None:
        if isFirstMove:
            return None
        kingsValley = game.board.getKingsValleyFieldCords()
        if isKing and self.moveTo["x"] == kingsValley["x"] and self.moveTo["y"] == kingsValley["y"]:
            self.winningByKing = True

        if player is not None:
            kingsCords = game.board.getKingsCords()
            opponentKing = kingsCords["blackKing"] if player == game.whitePlayer else kingsCords["whiteKing"]
            playerKing = kingsCords["whiteKing"] if player == game.whitePlayer else kingsCords["blackKing"]
            opponentKingMoves = game.getMoves(opponentKing["x"], opponentKing["y"], True, False)
            playerKingMoves = game.getMoves(playerKing["x"], playerKing["y"], True, False)

            if len(opponentKingMoves) <= 1:
                if (
                        self.__isMoveNextToField(opponentKing["x"], opponentKing["y"]) is False and
                        self.__isMoveNextToField(opponentKing["x"], opponentKing["y"])
                ):
                    self.winning = True
            if len(playerKingMoves) <= 1 and isKing is False:
                if self.__isMoveNextToField(playerKing["x"], playerKing["y"]):
                    self.losing = True
        return None

    def __isMoveNextToField(self, fieldX: int, fieldY: int) -> bool:
        for direction in self.moveDirections:
            if self.moveTo["x"] + direction[0] == fieldX and self.moveTo["y"] + direction[1] == fieldY:
                return True

        return False
