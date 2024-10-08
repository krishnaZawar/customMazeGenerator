from UI.page import Page

from PyQt6.QtWidgets import QLabel, QPushButton, QWidget

class HomePage(Page):
    def __init__(self, parent : QWidget) -> None:
        super().__init__(parent)

        self.parent = parent

        self.CSS = self.getFileContents('css/homePage.css')

        # -----------------------------------------------build page-------------------------------------------------------------------------------

        self.labelDict = dict()
        self.buttonDict = dict()

        self.labelDict['pageTitle'] = QLabel("CUSTOM MAZE GENERATOR", self)
        self.labelDict['pageTitle'].setGeometry(350, 100, 800, 150)

        buttonWidth = 300
        buttonHeight = 100
        
        self.buttonDict['play'] = QPushButton("Play", self) 
        self.buttonDict['play'].setGeometry(600, 300, buttonWidth, buttonHeight)
        self.buttonDict['createMaze'] = QPushButton("Create Maze", self) 
        self.buttonDict['createMaze'].setGeometry(self.buttonDict['play'].x(), self.buttonDict['play'].y() + buttonHeight, buttonWidth, buttonHeight)
        self.buttonDict['exit'] = QPushButton("Exit", self) 
        self.buttonDict['exit'].setGeometry(self.buttonDict['createMaze'].x(), self.buttonDict['createMaze'].y() + buttonHeight, buttonWidth, buttonHeight)

        # -------------------------------------------------add styling---------------------------------------------------------------------------
        cssLocation = 'css/homePage.css'

        self.labelDict['pageTitle'].setStyleSheet(self.CSS)
        self.buttonDict['play'].setStyleSheet(self.CSS)
        self.buttonDict['createMaze'].setStyleSheet(self.CSS)
        self.buttonDict['exit'].setStyleSheet(self.CSS)

        # --------------------------------------------------------connect buttons----------------------------------------------------------------

        self.buttonDict['exit'].clicked.connect(lambda: self.parent.close())
        self.buttonDict['play'].clicked.connect(lambda: self.parent.showPage('mazeGamePage'))
        self.buttonDict['createMaze'].clicked.connect(lambda: self.parent.showPage('mazeBuilderPage'))

    def getFileContents(self, fileLocation : str) -> str:
        with open(fileLocation) as file:
            data = file.read()
        return data
