from PyQt6.QtWidgets import QGridLayout, QWidget, QLabel

from gameLogic.player import Player

from constants import GRID_SIZE

class GameGrid(QWidget):
    def __init__(self, parent : object, fileLocation : str) -> None:
        super().__init__(parent)

        self.CSS = self.getFileContents('css\grid.css')

        self.parent = parent
        
        try:
            with open(fileLocation) as file:
                data = file.read()
                tempArr = data.split('\n')
                tempArr.pop()
                self.arr = [row.split(',') for row in tempArr]
                self.arr = [[int(cell) for cell in row] for row in self.arr]
        except FileNotFoundError:
            self.initMazeGame()

        self.gridSize = len(self.arr)
        self.cellSize = (GRID_SIZE-100) // self.gridSize

        for row in range(self.gridSize):
            for col in range(self.gridSize):
                if self.arr[row][col] == 2:
                    self.endTileRow, self.endTileCol = row, col

        self.setFixedSize(GRID_SIZE, GRID_SIZE)

    def setPos(self, x : int, y : int) -> None:
        self.setGeometry(x, y, GRID_SIZE, GRID_SIZE)
        
    def initMazeGame(self) -> None:
        # temp init to avoid build conflicts
        self.arr = [
            [1]
        ]

    def placePlayer(self, player : Player, key : str = "") -> None:
        if not key:
            for row in range(self.gridSize):
                for col in range(self.gridSize):
                    if self.arr[row][col] == 3:
                        player.setPos(row, col)
                        return
                        
        row, col = player.row, player.col

        newRow, newCol = row, col

        if key == 'up':
            if row-1 >= 0 and not self.arr[row-1][col] == 0:
                self.gridLayout[row][col].setProperty('class', 'walkable')
                newRow = row-1
        if key == 'down':
            if row+1 < self.gridSize and not self.arr[row+1][col] == 0:
                self.gridLayout[row][col].setProperty('class', 'walkable')
                newRow = row+1
        if key == 'left':
            if col-1 >= 0 and not self.arr[row][col-1] == 0:
                self.gridLayout[row][col].setProperty('class', 'walkable')
                newCol = col-1
        if key == 'right':
            if col+1 < self.gridSize and not self.arr[row][col+1] == 0:
                self.gridLayout[row][col].setProperty('class', 'walkable')
                newCol = col+1
        
        player.setPos(newRow, newCol)

        self.gridLayout[newRow][newCol].setProperty('class', 'playerTile')

        self.gridLayout[row][col].setStyleSheet(self.CSS)
        self.gridLayout[newRow][newCol].setStyleSheet(self.CSS)
            
    def buildGrid(self):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout : list[list[QLabel]] = []

        for row in range(self.gridSize):
            self.gridLayout.append([])
            for col in range(self.gridSize):
                newCell = QLabel()
                newCell.setFixedSize(self.cellSize, self.cellSize)

                self.gridLayout[-1].append(newCell)

                if self.arr[row][col] == 0:
                    newCell.setProperty('class', 'wall')
                elif self.arr[row][col] == 1:
                    newCell.setProperty('class', 'walkable')
                elif self.arr[row][col] == 2:
                    newCell.setProperty('class', 'endTile')
                elif self.arr[row][col] == 3:
                    newCell.setProperty('class', 'playerTile')
        
                newCell.setStyleSheet(self.CSS)

                layout.addWidget(newCell, row, col)
        
        self.setLayout(layout)


    def getFileContents(self, fileLocation : str) -> str:
        with open(fileLocation) as file:
            data = file.read()
        return data