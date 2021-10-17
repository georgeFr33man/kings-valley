from game.Board import Board


class Game:
    # Game defaults
    boardWidth = 5
    boardHeight = 5

    def __init__(self):
        self.board = Board(self.boardWidth, self.boardHeight)

    def play(self):
        pass

    # Winning rules:
    # King pawn in in the center, or
    # Opponent's king has no available moves
    def isWinningState(self):
        kingsFieldXY = self.board.getKingsValleyField()
        kingsFieldVal = self.board.getFieldValue(kingsFieldXY["x"], kingsFieldXY["y"])
        if kingsFieldVal == self.board.whiteKing or kingsFieldVal == self.board.blackKing:
            return True

        # Todo: check if kings have available moves
        return False
