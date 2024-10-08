import csv

from UI.page import Page

from gameLogic.builderGrid import BuilderGrid

from PyQt6.QtWidgets import QInputDialog, QMessageBox
from PyQt6.QtWidgets import QPushButton, QWidget, QLabel
from PyQt6.QtWidgets import QGraphicsOpacityEffect

class MazeBuilderPage(Page):
    def __init__(self, parent : QWidget) -> None:
        super().__init__(parent)

        self.parent = parent

        self.selectedOpacity = 1
        self.normalOpacity = 0.2

        self.CSS = self.getFileContents('css/buttons.css')
        self.curSelection : QPushButton = None

        self.initBuilderButtons()
        self.buildGrid(5)
        self.activateBuilder(False)
        
        self.initGridChoiceButtonsPage()
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
    
    def applyOpacityEffect(self, widget : QWidget, opacity : int) -> None:
        opacityObject = QGraphicsOpacityEffect()
        opacityObject.setOpacity(opacity)
        widget.setGraphicsEffect(opacityObject)

    def handlePages(self) -> None:
        if self.curPage == 'builderPage':
            self.activateGridChoicePage(True)
        else:
            self.parent.showPage('homePage')

# --------------------------------------------------builder page-------------------------------------------------------------------------------

    def activateBuilder(self, choice : bool, size : int = 0) -> None:
        if choice:
            self.curPage = 'builderPage'
            self.activateGridChoicePage(False)
            self.buildGrid(size)
        self.activateWidget(self.curGrid, choice)
        self.activateWidget(self.playerButton, choice)
        self.activateWidget(self.wallButton, choice)
        self.activateWidget(self.endTileButton, choice)
        self.activateWidget(self.eraseButton, choice)
        self.activateWidget(self.saveButton, choice)
    
    def buildGrid(self, gridSize : int) -> None:
        self.curGrid = BuilderGrid(self, gridSize)
        self.curGrid.initMazeBuilder()
        self.curGrid.buildGrid()
        self.curGrid.setPos(200, 100)
    
    def initBuilderButtons(self) -> None:
        self.playerButton = QPushButton(self)
        self.wallButton = QPushButton(self)
        self.endTileButton = QPushButton(self)
        self.eraseButton = QPushButton(self)
        self.saveButton = QPushButton("Save", self)

        buttonSize = 100
        buttonGap = buttonSize + 25

        self.playerButton.setGeometry(1200, 100, buttonSize, buttonSize)
        self.wallButton.setGeometry(self.playerButton.x(), self.playerButton.y() + buttonGap, buttonSize, buttonSize)
        self.endTileButton.setGeometry(self.playerButton.x(), self.wallButton.y() + buttonGap, buttonSize, buttonSize)
        self.eraseButton.setGeometry(self.playerButton.x(), self.endTileButton.y() + buttonGap, buttonSize, buttonSize)
        self.saveButton.setGeometry(self.playerButton.x(), self.eraseButton.y() + buttonGap, buttonSize, buttonSize)

        self.playerButton.setObjectName('playerButton')
        self.wallButton.setObjectName('wallButton')
        self.endTileButton.setObjectName('endTileButton')
        self.eraseButton.setObjectName('eraseButton')
        self.saveButton.setObjectName('saveButton')

        self.playerButton.setStyleSheet(self.CSS)
        self.wallButton.setStyleSheet(self.CSS)
        self.endTileButton.setStyleSheet(self.CSS)
        self.eraseButton.setStyleSheet(self.CSS)
        self.saveButton.setStyleSheet(self.CSS)

        self.applyOpacityEffect(self.playerButton, self.normalOpacity)
        self.applyOpacityEffect(self.wallButton, self.normalOpacity)
        self.applyOpacityEffect(self.endTileButton, self.normalOpacity)
        self.applyOpacityEffect(self.eraseButton, self.normalOpacity)


        self.playerButton.clicked.connect(lambda: self.onClickBuilderButton(self.playerButton))
        self.wallButton.clicked.connect(lambda: self.onClickBuilderButton(self.wallButton))
        self.endTileButton.clicked.connect(lambda: self.onClickBuilderButton(self.endTileButton))
        self.eraseButton.clicked.connect(lambda: self.onClickBuilderButton(self.eraseButton))
        self.saveButton.clicked.connect(self.onClickSaveButton)
    
    def onClickSaveButton(self) -> None:
        if self.curGrid.numPlayers == 0:
            QMessageBox(text='place a player first').exec()
            return
        elif self.curGrid.numEndTiles == 0:
            QMessageBox(text='place a endpoint first.').exec()
            return
        dialog = QInputDialog(self)
        dialog.setOkButtonText('Save')
        dialog.setCancelButtonText('Cancel')

        fileName, shouldSave = dialog.getText(self, 'save grid', 'enter file name')

        if not shouldSave:
            return
        
        fileLoc = f'mazes/{self.curGrid.gridSize}x{self.curGrid.gridSize}/{fileName}.csv'
        try:
            with open(fileLoc) as file:
                shouldReplace = QMessageBox.question(self, 'warning', f'do you want to replace the file {fileName}', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
                if shouldReplace == QMessageBox.StandardButton.No:
                    return
        except:
            with open(fileLoc, "w", newline='') as file:
                csvWriter = csv.writer(file)
                csvWriter.writerows(self.curGrid.arr)
        
        self.activateGridChoicePage(True)


    def onClickBuilderButton(self, button : QPushButton) -> None:
        if self.curSelection:
            self.applyOpacityEffect(self.curSelection, self.normalOpacity)
        self.applyOpacityEffect(button, self.selectedOpacity)
        self.curSelection = button

    def updateGrid(self, row : int, col : int) -> None:
        if not self.curSelection:
            return
        objectType = self.curSelection.objectName()

        if objectType == 'playerButton':
            if self.curGrid.numPlayers:
                return
            cellType = 'playerTile'
        elif objectType == 'endTileButton':
            if self.curGrid.numEndTiles:
                return
            cellType = 'endTile'
        elif objectType == 'wallButton':
            cellType = 'wall'
        elif objectType == 'eraseButton':
            cellType = 'walkable'
        
        self.curGrid.placeCell(row, col, cellType)
        
    # ---------------------------------------------------grid choice page------------------------------------------------------------------------

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
            self.gridButtons[f'{i}x{i}'].clicked.connect(lambda check, size = i: self.activateBuilder(True, size))

    def activateGridChoicePage(self, choice : bool) -> None:
        if choice:
            self.curPage = 'gridChoicePage'
            self.activateBuilder(False)
        self.activateWidget(self.gridChoiceLabel, choice)
        for key in self.gridButtons:
            self.activateWidget(self.gridButtons[key], choice)