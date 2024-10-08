from PyQt6.QtWidgets import QMainWindow

from UI import homePage, mazeBuilderPage, mazeGamePage, page

from constants import WINDOW_HEIGHT, WINDOW_WIDTH

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setGeometry(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

        self.homePage = homePage.HomePage(self)
        self.mazeBuilderPage = mazeBuilderPage.MazeBuilderPage(self)
        self.mazeGamePage = mazeGamePage.MazeGamePage(self)

        self.showPage('homePage')

        self.show()

    def activatePage(self, page : page.Page, choice : bool) -> None:
        page.setEnabled(choice)
        page.setVisible(choice)
    def showPage(self, page : str) -> None:
        self.activatePage(self.homePage, False)
        self.activatePage(self.mazeGamePage, False)
        self.activatePage(self.mazeBuilderPage, False)
        if  page == 'homePage':
            self.activatePage(self.homePage, True)
        elif page == 'mazeBuilderPage':
            self.activatePage(self.mazeBuilderPage, True)
            self.mazeBuilderPage.activateGridChoicePage(True)
        elif page == 'mazeGamePage':
            self.activatePage(self.mazeGamePage, True)
            self.mazeGamePage.activateGridChoicePage(True)