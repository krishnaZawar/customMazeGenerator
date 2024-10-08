class Player():
    def __init__(self):
        self.row = 0
        self.col = 0

    def setPos(self, row : int, col : int) -> None:
        self.row = row
        self.col = col