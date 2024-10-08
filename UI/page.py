from PyQt6.QtWidgets import QFrame, QMainWindow
from constants import *

class Page(QFrame):
    def __init__(self, parent : object) -> None:
        super().__init__(parent) 

        self.setGeometry(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    def getPageWidth(self) -> int:
        return self.width()

    def getPageHeight(self) -> int:
        return self.height()