from PyQt6.QtWidgets import QGridLayout, QWidget, QPushButton

from constants import GRID_SIZE

class BuilderGrid(QWidget):
    def __init__(self, parent : object, gridSize : int = 5) -> None:
        super().__init__(parent)

        self.CSS = self.getFileContents('css/grid.css')

        self.parent = parent

        self.gridSize = gridSize

        self.cellSize = (GRID_SIZE-100) // gridSize

        self.setFixedSize(GRID_SIZE, GRID_SIZE)

        self.numPlayers = 0
        self.numEndTiles = 0

    def setPos(self, x : int, y : int) -> None:
        self.setGeometry(x, y, GRID_SIZE, GRID_SIZE)

    def initMazeBuilder(self) -> None:
        self.arr = [[1 for i in range(self.gridSize)] for j in range(self.gridSize)]

    def placeCell(self, row : int, col : int, cellType : str) -> None:
        if self.arr[row][col] == 3:
            self.numPlayers -= 1
        if self.arr[row][col] == 2:
            self.numEndTiles -= 1

        if cellType == 'walkable':
            self.arr[row][col] = 1
        elif cellType == 'wall':
            self.arr[row][col] = 0
        elif cellType == 'endTile':
            self.numEndTiles += 1
            self.arr[row][col] = 2
        elif cellType == 'playerTile':
            self.numPlayers += 1
            self.arr[row][col] = 3
        self.gridLayout[row][col].setProperty('class', cellType)
        self.gridLayout[row][col].setStyleSheet(self.CSS)

    def buildGrid(self):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout : list[list[QPushButton]] = []

        for row in range(self.gridSize):
            self.gridLayout.append([])
            for col in range(self.gridSize):
                newCell = QPushButton()
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

                self.gridLayout[-1][-1].clicked.connect(lambda check, r = row, c = col: self.parent.updateGrid(r, c))

                layout.addWidget(newCell, row, col)
        
        self.setLayout(layout)

    def getFileContents(self, fileLocation : str) -> str:
        with open(fileLocation) as file:
            data = file.read()
        return data