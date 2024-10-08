from UI.page import Page

from gameLogic.gameGrid import GameGrid
from gameLogic.player import Player

import os

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QLabel, QPushButton, QWidget, QScrollArea, QVBoxLayout, QMessageBox

from PyQt6.QtGui import QShortcut, QKeySequence

class MazeGamePage(Page):
    def __init__(self, parent : QWidget) -> None:
        super().__init__(parent)

        self.parent = parent

        # -----------------------------------------------build page---------------------------------------------------------------------------
        self.CSS = self.getFileContents('css/buttons.css')

        self.player = Player()

        self.buildGrid()
        self.connectKeys()

        self.initGridChoiceButtonsPage()

        self.initMazeSelectionPage()

        self.activateGridChoicePage(True)
        
        self.backButton = QPushButton("Back", self)
        self.backButton.setGeometry(25, 25, 100, 75)
        self.backButton.setObjectName('backButton')
        self.backButton.setStyleSheet(self.CSS)
        self.backButton.clicked.connect(self.handlePages)


    def getFileContents(self, fileLocation : str) -> str:
        with open(fileLocation) as file:
            data = file.read()
        return data
    
    def activateWidget(self, widget : QWidget, choice : bool) -> None:
        widget.setEnabled(choice)
        widget.setVisible(choice)

    def handlePages(self) -> None:
        if self.curPage == 'gamePage':
            self.activateMazeSelectionPage(True)
        elif self.curPage == 'mazeSelectionPage':
            self.activateGridChoicePage(True)
        else:
            self.parent.showPage('homePage')

# ---------------------------------------------------------select grid page-------------------------------------------------------------------

    def initGridChoiceButtonsPage(self) -> None:
        self.gridChoiceLabel = QLabel("Select Grid Size", self)
        self.gridChoiceLabel.setGeometry(600, 100, 600, 100)
        self.gridChoiceLabel.setStyleSheet(self.CSS)

        self.gridButtons = dict()
        self.gridButtons['2x2'] = QPushButton("2x2", self)
        self.gridButtons['3x3'] = QPushButton("3x3", self)
        self.gridButtons['4x4'] = QPushButton("4x4", self)
        self.gridButtons['5x5'] = QPushButton("5x5", self)
        self.gridButtons['6x6'] = QPushButton("6x6", self)
        self.gridButtons['7x7'] = QPushButton("7x7", self)
        self.gridButtons['8x8'] = QPushButton("8x8", self)
        self.gridButtons['9x9'] = QPushButton("9x9", self)
        self.gridButtons['10x10'] = QPushButton("10x10", self)
        self.gridButtons['11x11'] = QPushButton("11x11", self)

        buttonSize = 100
        buttonXGap = buttonSize + 100
        buttonYGap = buttonSize + 25

        self.gridButtons['2x2'].setGeometry(300, 300, buttonSize, buttonSize)
        self.gridButtons['3x3'].setGeometry(self.gridButtons['2x2'].x() + buttonXGap, self.gridButtons['2x2'].y(), buttonSize, buttonSize)
        self.gridButtons['4x4'].setGeometry(self.gridButtons['3x3'].x() + buttonXGap, self.gridButtons['2x2'].y(), buttonSize, buttonSize)
        self.gridButtons['5x5'].setGeometry(self.gridButtons['4x4'].x() + buttonXGap, self.gridButtons['2x2'].y(), buttonSize, buttonSize)
        self.gridButtons['6x6'].setGeometry(self.gridButtons['5x5'].x() + buttonXGap, self.gridButtons['2x2'].y(), buttonSize, buttonSize)
        self.gridButtons['7x7'].setGeometry(self.gridButtons['2x2'].x(), self.gridButtons['2x2'].y() + buttonYGap, buttonSize, buttonSize)
        self.gridButtons['8x8'].setGeometry(self.gridButtons['7x7'].x() + buttonXGap, self.gridButtons['2x2'].y() + buttonYGap, buttonSize, buttonSize)
        self.gridButtons['9x9'].setGeometry(self.gridButtons['8x8'].x() + buttonXGap, self.gridButtons['2x2'].y() + buttonYGap, buttonSize, buttonSize)
        self.gridButtons['10x10'].setGeometry(self.gridButtons['9x9'].x() + buttonXGap, self.gridButtons['2x2'].y() + buttonYGap, buttonSize, buttonSize)
        self.gridButtons['11x11'].setGeometry(self.gridButtons['10x10'].x() + buttonXGap, self.gridButtons['2x2'].y() + buttonYGap, buttonSize, buttonSize)

        for key in self.gridButtons:
            self.gridButtons[key].setProperty('class', 'gridButton')
            self.gridButtons[key].setStyleSheet(self.CSS)

        for i in range(2, 12):
            self.gridButtons[f'{i}x{i}'].clicked.connect(lambda check, size = i: self.activateMazeSelectionPage(True, size))

    def activateGridChoicePage(self, choice : bool) -> None:
        if choice:
            self.activateMazeSelectionPage(False)
            self.activateGamePage(False)
            self.curPage = 'gridChoicePage'
        self.activateWidget(self.gridChoiceLabel, choice)
        for key in self.gridButtons:
            self.activateWidget(self.gridButtons[key], choice)

# ------------------------------------------------------------select maze page--------------------------------------------------------------

    def buildScrollArea(self, gridSize : int) -> None:
        self.fileScrollArea = QScrollArea(self)
        self.fileScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.fileScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.fileScrollArea.setGeometry(400, 100, 500, 800)
        self.fileScrollArea.setWidgetResizable(True)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        folderLoc = f'mazes/{gridSize}x{gridSize}'

        files : list[str] = os.listdir(folderLoc)

        fileNames : list[str] = [file[0:(len(file)-4)] for file in files]

        for fileName in fileNames:
            playButton = QPushButton()     
            playButton.setMinimumHeight(30)       
            playButton.setText(f"{fileName}")
            playButton.clicked.connect(lambda check, mazeFile = f'{folderLoc}/{fileName}.csv': self.activateGamePage(True, mazeFile))
            layout.addWidget(playButton)
        
        widget.setLayout(layout)
        self.fileScrollArea.setWidget(widget)

        self.fileScrollArea.setStyleSheet(self.getFileContents('css/scrollArea.css'))

    def initMazeSelectionPage(self, gridSize : int = 2) -> None:
        self.selectMazeLabel = QLabel("Select Maze", self)
        self.selectMazeLabel.setGeometry(500, 25, 500, 75)
        self.selectMazeLabel.setStyleSheet('font : 50px;')
        self.buildScrollArea(gridSize)

    def activateMazeSelectionPage(self, choice : bool, gridSize : int = 2) -> None:
        if choice:
            self.curPage = 'mazeSelectionPage'
            self.buildScrollArea(gridSize)
            self.activateGamePage(False)
            self.activateGridChoicePage(False)
        self.activateWidget(self.fileScrollArea, choice)
        self.activateWidget(self.selectMazeLabel, choice)
# ------------------------------------------------------------game page------------------------------------------------------------------------
    
    def activateGamePage(self, choice : bool, fileName : str = '') -> None:
        if choice:
            self.curPage = 'gamePage'
            self.buildGrid(fileName)
            self.activateMazeSelectionPage(False)
            self.activateGridChoicePage(False)
        self.activateWidget(self.curGrid, choice)
        self.upKeys.setEnabled(choice)
        self.downKeys.setEnabled(choice)
        self.rightKeys.setEnabled(choice)
        self.leftKeys.setEnabled(choice)

    def buildGrid(self, fileName : str = ''):
        self.curGrid = GameGrid(self, fileName)
        self.curGrid.buildGrid()
        self.curGrid.setPos(400, 100)
        self.curGrid.placePlayer(self.player)

    def connectKeys(self) -> None:
        self.upKeys = QShortcut(self)
        self.upKeys.setKeys([QKeySequence("w"), QKeySequence("up")])
        self.upKeys.setEnabled(True)

        self.downKeys = QShortcut(self)
        self.downKeys.setKeys([QKeySequence("s"), QKeySequence("down")])
        self.downKeys.setEnabled(True)

        self.leftKeys = QShortcut(self)
        self.leftKeys.setKeys([QKeySequence("a"), QKeySequence("left")])
        self.leftKeys.setEnabled(True)

        self.rightKeys = QShortcut(self)
        self.rightKeys.setKeys([QKeySequence("d"), QKeySequence("right")])
        self.rightKeys.setEnabled(True)

        self.upKeys.activated.connect(lambda move = 'up': self.handleGameMovement(move))
        self.downKeys.activated.connect(lambda move = 'down': self.handleGameMovement(move))
        self.leftKeys.activated.connect(lambda move = 'left': self.handleGameMovement(move))
        self.rightKeys.activated.connect(lambda move = 'right': self.handleGameMovement(move))

    def handleGameMovement(self, move : str) -> None:
        self.curGrid.placePlayer(self.player, move)

        if self.player.row == self.curGrid.endTileRow and self.player.col == self.curGrid.endTileCol:
            QMessageBox(text='Congratulations!! You completed the maze.').exec()
            self.parent.showPage('homePage')