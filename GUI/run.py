import sys

from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

sys.path.insert(1, '/envTest')
from envTest.detection import detect
from envTest.extract import extract


# class MediaPlayer(QtWidgets.QWidget):
#     def __init__(self, logger, parent=None):
#         super(MediaPlayer, self).__init__(parent)
#
#         self.setGeometry(0, 0, 640, 480)
#
#         self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
#
#         self.videoWidget = QVideoWidget(self)
#         self.videoWidget.setGeometry(0, 0, 640, 480)
#         # self.setStyleSheet("border: 1px solid;")
#         # p = self.videoWidget.palette()
#         # p.setColor(self.videoWidget.backgroundRole(), QtCore.Qt.black)
#         # self.videoWidget.setPalette(p)
#
#         # Control Bar Elements
#         self.playButton = QtWidgets.QPushButton()
#         self.playButton.setEnabled(False)
#         self.playButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
#         self.playButton.clicked.connect(self.play)
#
#         self.rateUp = QtWidgets.QPushButton()
#         self.rateUp.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaSeekForward))
#         self.rateUp.clicked.connect(self.rate_up)
#         self.rateDown = QtWidgets.QPushButton()
#         self.rateDown.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaSeekBackward))
#         self.rateDown.clicked.connect(self.rate_down)
#         self.rate = 1.0
#         self.rateLabel = QtWidgets.QLabel('x' + "%.1f" % self.rate)
#
#         self.positionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
#         self.positionSlider.setRange(0, 0)
#         self.positionSlider.sliderMoved.connect(self.set_position)
#
#         self.error = QtWidgets.QLabel()
#         self.error.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
#
#         self.controlPanel = QtWidgets.QFrame(self)
#         self.controlPanel.setGeometry(QtCore.QRect(0, self.height() - 24, self.width(), 24))
#         self.controlLayout = QtWidgets.QHBoxLayout()
#         self.controlLayout.setContentsMargins(0, 0, 0, 0)
#         self.controlLayout.addWidget(self.playButton)
#         self.controlLayout.addWidget(self.positionSlider)
#         self.controlLayout.addWidget(self.rateDown)
#         self.controlLayout.addWidget(self.rateLabel)
#         self.controlLayout.addWidget(self.rateUp)
#
#         self.controlPanel.setLayout(self.controlLayout)
#
#         self.mediaPlayer.setVideoOutput(self.videoWidget)
#         self.mediaPlayer.stateChanged.connect(self.media_state_changed)
#         self.mediaPlayer.positionChanged.connect(self.position_changed)
#         self.mediaPlayer.durationChanged.connect(self.duration_changed)
#         self.mediaPlayer.error.connect(self.handle_error)
#
#     def open_file(self):
#         fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
#                                                             r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\footage_video")
#
#         if fileName != '':
#             self.mediaPlayer.setMedia(
#                 QMediaContent(QtCore.QUrl.fromLocalFile(fileName)))
#             self.playButton.setEnabled(True)
#
#     @staticmethod
#     def exit_call():
#         sys.exit(app.exec_())
#
#     def play(self):
#         if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
#             self.mediaPlayer.pause()
#         else:
#             self.mediaPlayer.play()
#
#     def rate_up(self):
#         self.rate += 0.1
#         self.mediaPlayer.setPlaybackRate(self.rate)
#         self.rateLabel.setText('x' + "%.1f" % self.rate)
#
#     def rate_down(self):
#         self.rate -= 0.1
#         if self.rate < 0.1:
#             self.rate = 0.1
#         self.mediaPlayer.setPlaybackRate(self.rate)
#         self.rateLabel.setText('x' + "%.1f" % self.rate)
#
#     def media_state_changed(self):
#         if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
#             self.playButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
#         else:
#             self.playButton.setIcon(
#                 self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
#
#     def position_changed(self, position):
#         self.positionSlider.setValue(position)
#
#     def duration_changed(self, duration):
#         self.positionSlider.setRange(0, duration)
#
#     def set_position(self, position):
#         self.mediaPlayer.set_position(position)
#
#     def handle_error(self):
#         self.playButton.setEnabled(False)
#         self.error.setText("Error: " + self.mediaPlayer.errorString())
#
#
# class VideoFrame(QtWidgets.QWidget):
#     def __init__(self, logger, parent=None):
#         super(VideoFrame, self).__init__(parent)
#         self.logger = logger
#
#         self.mediaPlayer = MediaPlayer(logger, self)
#
#         self.frame = QtWidgets.QFrame(self)
#         # self.mediaPlayer.hide()
#
#         self.fig = plt.figure(figsize=(8, 8))
#         ax = plt.axes(projection='3d')
#         import numpy as np
#         from scipy import signal
#         t = np.linspace(0, 1, 1000, endpoint=True)
#         ax.plot3D(t, signal.square(2 * np.pi * 5 * t))
#
#         ax.patch.set_alpha(0.0)
#         ax.set_axis_off()
#         self.fig.patch.set_alpha(0.0)
#
#         self.canvas = FigureCanvas(self.fig)
#         self.canvas.setStyleSheet("background: transparent;")
#
#         self.frame.setLayout(QtWidgets.QVBoxLayout())
#         self.frame.layout().addWidget(self.canvas)
#         self.frame.setStyleSheet("background: transparent;")
#


class VideoFrame(QtWidgets.QWidget):
    def __init__(self, logger, parent=None):
        super(VideoFrame, self).__init__(parent)
        self.resize(640, 480)

        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.videoItem = QtMultimediaWidgets.QGraphicsVideoItem()
        self.scene.addItem(self.videoItem)

        self.view.setInteractive(False)

        fig = plt.figure(figsize=(31, 23), dpi=20)
        ax = plt.axes(projection='3d')
        import numpy as np
        from scipy import signal
        t = np.linspace(0, 1, 1000, endpoint=True)
        ax.plot3D(t, signal.square(2 * np.pi * 5 * t))
        ax.patch.set_alpha(0.0)
        ax.set_axis_off()
        fig.patch.set_alpha(0.0)
        canvas = FigureCanvas(fig)
        canvas.draw()
        pixmap = QtGui.QPixmap(QtGui.QImage(canvas.buffer_rgba(), canvas.size().width(), canvas.size().height(),
                                            QtGui.QImage.Format_ARGB32))
        self.scene.addPixmap(pixmap)

        self.mediaPlayer = QtMultimedia.QMediaPlayer(self, QtMultimedia.QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.videoItem)

        self.view.resize(640, 480)
        self.videoItem.setPos(0, 0)
        self.videoItem.setScale(1.8)
        self.view.show()


    def open_file(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
                                                            r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\footage_video")
        if fileName != '':
            self.mediaPlayer.setMedia(
                QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(fileName)))

    def play(self):
        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()






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


class Processus(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Processus, self).__init__(parent)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.name = QtWidgets.QLabel("temp")
        self.button = QtWidgets.QPushButton(">")
        self.parameterLayout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.name, 0, 0)
        self.layout.addWidget(self.button, 0, 1)
        self.layout.addLayout(self.parameterLayout, 1, 0, 2, 4)
        self.layout.setColumnStretch(0, 3)
        self.layout.setColumnStretch(1, 1)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 3)

    def init_values(self, name, function, parameters):
        self.name.setText(name)
        self.button.clicked.connect(function)

        for parameter in parameters:
            item_layout = QtWidgets.QHBoxLayout()
            if parameter[1] == "checkbox":
                new_param = QtWidgets.QCheckBox(parameter[0])
                item_layout.addWidget(new_param)
            elif parameter[1] == "slider":
                new_param = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
                item_layout.addWidget(QtWidgets.QLabel(parameter[0]))
                item_layout.addWidget(new_param)
            elif parameter[1] == "textinput":
                new_param = QtWidgets.QTextEdit()
                item_layout.addWidget(new_param)
            self.parameterLayout.addLayout(item_layout)


class ProcessFrame(QtWidgets.QWidget):
    def __init__(self, logger, parent=None):
        super(ProcessFrame, self).__init__(parent)
        self.logger = logger

        # Window init
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        # Temporary
        fileOpenParams = [
            ["temp", "checkbox"],
            ["temp3", "checkbox"],
            ["temp4", "checkbox"],
            ["temp5", "slider"]
        ]

        # Initialising all modules
        self.fileProcess = Processus(self)
        self.trackProcess = Processus(self)
        self.trajProcess = Processus(self)
        self.fileProcess.init_values("Load Video", parent.videoFrame.open_file, fileOpenParams)
        self.trackProcess.init_values("Track", detect, [])
        self.trajProcess.init_values("Extract Trajectory", extract, [])

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
        self.videoFrame = VideoFrame(logger, self)
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

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_E:
            self.videoFrame.play()
        elif e.key() == QtCore.Qt.Key_R:
            self.videoFrame.open_file()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Application")
    window.show()
    sys.exit(app.exec_())
