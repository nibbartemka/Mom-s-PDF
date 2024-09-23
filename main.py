import sys

from PyQt6.QtWidgets import (
    QApplication,
)

from GUI.MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    screen = MainWindow()
    screen.show()
    app.exec()


if __name__ == '__main__':
    main()
