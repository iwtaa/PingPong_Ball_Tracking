from PyQt6.QtWidgets import *
from PyQt6.QtQml import *


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.load('./main.qml')

    sys.exit(app.exec())
