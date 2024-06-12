import sys

from PyQt5 import QtWidgets, QtCore

import matplotlib.pyplot as plt

sys.path.insert(1, 'functions')
sys.path.insert(1, '/')
sys.path.insert(1, '/visualisations')

from videoplayer import VideoPlayer
from parameters import Parameters
from visualisations.trajectoryParameters import TrajectoryParameters
from visualisations.videoParameters import VideoParameters
from GUI.processes.OpenVideoProcess import ProcessusOpenFile
from GUI.processes.DetectionProcess import ProcessusDetection
from globalData import Global

globalparams = Global()


class Console(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super(Console, self).__init__(parent)

        self.setReadOnly(True)

    def log(self, text):
        self.append(text + '\n')


class ProcessFrame(QtWidgets.QWidget):
    def __init__(self, mediaPlayer, parent=None):
        super(ProcessFrame, self).__init__(parent)
        self.parent = parent

        # Window init
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        globalparams.data["tempparam"] = "testingparameters"
        # Initialising all modules
        self.fileProcess = ProcessusOpenFile(globalparams, mediaPlayer, self)
        self.trackProcess = ProcessusDetection(globalparams, mediaPlayer, self)

        self.layout.addWidget(self.fileProcess)
        self.layout.addWidget(self.trackProcess)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Window init
        self.resize(894, 659)

        # Frames
        self.parametersFrame = Parameters(globalparams, self)
        self.videoParameters = VideoParameters(globalparams, self.parametersFrame)
        self.trajectoryParameters = TrajectoryParameters(globalparams, self.parametersFrame)
        self.videoFrame = VideoPlayer(globalparams, self)
        self.processFrame = ProcessFrame(self.videoFrame.mediaPlayer, self)
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


if __name__ == "__main__":
    plt.switch_backend('agg')
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Application")
    window.show()
    sys.exit(app.exec_())
