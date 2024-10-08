import sys

from PyQt6.QtWidgets import QApplication

from mainWindow import MainWindow

def main() -> None:
    app = QApplication(sys.argv)

    window = MainWindow()

    app.exec()

if __name__ == '__main__':
    main()