import sys

from PyQt5 import QtWidgets, QtCore

import matplotlib.pyplot as plt

sys.path.insert(1, '/envTest')

from videoplayer import VideoPlayer
from OpenVideoProcess import ProcessusOpenFile
from DetectionProcess import ProcessusDetection
from globalData import Global

globalparams = Global()


class ParametersFrame(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ParametersFrame, self).__init__(parent)

        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.setGeometry(QtCore.QRect(0, 0, 209, 400))

        self.tab1 = QtWidgets.QFrame(self.tabs)
        self.tab2 = QtWidgets.QFrame(self.tabs)
        self.tab1.setGeometry(QtCore.QRect(0, 0, 209, 480))
        self.tab2.setGeometry(QtCore.QRect(0, 0, 209, 480))
        self.tab1_layout = QtWidgets.QVBoxLayout()
        self.tab2_layout = QtWidgets.QVBoxLayout()
        self.tab1.setLayout(self.tab1_layout)
        self.tab2.setLayout(self.tab2_layout)
        self.tab1_layout.setContentsMargins(0, 0, 0, 0)
        self.tab1_layout.setSpacing(0)
        self.tab2_layout.setContentsMargins(0, 0, 0, 0)
        self.tab2_layout.setSpacing(0)

        self.temp1 = QtWidgets.QLabel("test1")
        self.temp2 = QtWidgets.QLabel("test2")
        self.temp3 = QtWidgets.QLabel("test3")
        self.temp4 = QtWidgets.QLabel("test4")
        self.temp5 = QtWidgets.QLabel("test5")
        self.temp6 = QtWidgets.QLabel("test6")
        self.temp7 = QtWidgets.QLabel("test7")
        self.temp8 = QtWidgets.QLabel("test8")

        self.tab1_layout.addWidget(self.temp1)
        self.tab1_layout.addWidget(self.temp2)
        self.tab1_layout.addWidget(self.temp3)
        self.tab2_layout.addWidget(self.temp4)
        self.tab2_layout.addWidget(self.temp5)
        self.tab2_layout.addWidget(self.temp6)
        self.tab2_layout.addWidget(self.temp7)
        self.tab2_layout.addWidget(self.temp8)

        self.tabs.addTab(self.tab1, "tab1")
        self.tabs.addTab(self.tab2, "tab2")

        self.console = Console(self)
        self.console.setGeometry(QtCore.QRect(0, 400, 209, 80))


class Console(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super(Console, self).__init__(parent)

        self.setReadOnly(True)

    def log(self, text):
        self.append(text + '\n')


class ProcessFrame(QtWidgets.QWidget):
    def __init__(self, logger, parent=None):
        super(ProcessFrame, self).__init__(parent)
        self.logger = logger
        self.parent = parent

        # Window init
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        globalparams.data["tempparam"] = "testingparameters"
        # Initialising all modules
        self.fileProcess = ProcessusOpenFile(globalparams, self)
        self.trackProcess = ProcessusDetection(globalparams, self)
        self.trajProcess = ProcessusOpenFile(globalparams, self)

        self.layout.addWidget(self.fileProcess)
        self.layout.addWidget(self.trackProcess)
        self.layout.addWidget(self.trajProcess)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Window init
        self.resize(894, 659)

        # Frames
        self.parametersFrame = ParametersFrame(self)
        logger = self.parametersFrame.console.log
        self.videoFrame = VideoPlayer(globalparams, self)
        self.processFrame = ProcessFrame(logger, self)
        self.videoFrame.setGeometry(15, 40, 640, 480)
        self.parametersFrame.setGeometry(670, 40, 209, 480)
        self.processFrame.setGeometry(15, 536, 864, 100)

        # Menus
        # self.menu_files = self.menuBar().addMenu("Files")
        # self.menu_files.addAction("Open Video")
        self.toolbar = QtWidgets.QToolBar("test")
        self.addToolBar(self.toolbar)

        openfile_action = QtWidgets.QAction("Open File", self)
        openfile_action.triggered.connect(self.videoFrame.open_file)
        self.toolbar.addAction(openfile_action)

    def keyPressEvent(self, e, **kwargs):
        if e.key() == QtCore.Qt.Key_E:
            self.videoFrame.pause_signal.emit()
        elif e.key() == QtCore.Qt.Key_R:
            self.videoFrame.open_file()
        elif e.key() == QtCore.Qt.Key_D:
            self.videoFrame.frame_back_signal.emit()
        elif e.key() == QtCore.Qt.Key_F:
            self.videoFrame.frame_next_signal.emit()


if __name__ == "__main__":
    plt.switch_backend('agg')
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Application")
    window.show()
    sys.exit(app.exec_())
