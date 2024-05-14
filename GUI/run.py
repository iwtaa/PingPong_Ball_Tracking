import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

sys.path.insert(1, '/envTest')
from envTest.detection import detect
from envTest.extract import extract

class oldVideoFrame(QWidget):
    def __init__(self, parent=None):
        super(oldVideoFrame, self).__init__(parent)
        self.openButton = QPushButton("Open Video", self)
        self.openButton.setGeometry(QRect(self.width() - 70, self.height() - 24, 70, 24))
        self.openButton.setToolTip("Open Video File")
        self.openButton.setStatusTip("Open Video File")
        self.openButton.setFixedHeight(24)
        self.openButton.clicked.connect(self.openFile)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.videoWidget = QVideoWidget(self)
        self.videoWidget.setGeometry(0, 0, 640, 456)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.error = QLabel()
        self.error.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.controlPanel = QFrame(self)
        self.controlPanel.setGeometry(QRect(0, self.height() - 24, self.width() - 70, 24))
        self.controlLayout = QHBoxLayout()
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.positionSlider)
        self.controlPanel.setLayout(self.controlLayout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                                                  QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.error.setText("Error: " + self.mediaPlayer.errorString())


class oldMainFrame(QWidget):
    def __init__(self, parent=None):
        super(oldMainFrame, self).__init__(parent)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 50, 640, 480))
        self.label.setStyleSheet("border: 1px solid;")

        self.actionButtons = QFrame(self)
        self.actionButtons.setGeometry(QRect(0, 0, 640, 50))
        self.actionButtons_layout = QHBoxLayout()
        self.actionButtons.setLayout(self.actionButtons_layout)
        self.actionButtons_layout.setContentsMargins(0, 0, 0, 0)
        self.actionButtons_layout.setSpacing(0)
        self.temp1 = QPushButton("test1")
        self.temp1.setMinimumHeight(50)
        self.temp2 = QPushButton("test3")
        self.temp2.setMinimumHeight(50)
        self.temp3 = QPushButton("test2")
        self.temp3.setMinimumHeight(50)
        self.actionButtons_layout.addWidget(self.temp1)
        self.actionButtons_layout.addWidget(self.temp2)
        self.actionButtons_layout.addWidget(self.temp3)

        # th = VideoPlayer(self)
        # th.init(loadVideo())
        # th.changePixmap.connect(self.setImage)
        # th.start()
        self.wid = oldVideoFrame(self)
        self.wid.setGeometry(QRect(0, 50, 640, 480))


class oldParameterFrame(QWidget):
    def __init__(self, parent=None):
        super(oldParameterFrame, self).__init__(parent)

        self.frame = QFrame(self)
        self.layout = QHBoxLayout()
        self.frame.setLayout(self.layout)

        self.frame.resize(160, 530)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.parameterTabs = QTabWidget()

        self.tab1 = QFrame(self.parameterTabs)
        self.tab2 = QFrame(self.parameterTabs)
        self.tab1_layout = QVBoxLayout()
        self.tab2_layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1_layout)
        self.tab2.setLayout(self.tab2_layout)
        self.tab1_layout.setContentsMargins(0, 0, 0, 0)
        self.tab1_layout.setSpacing(0)
        self.tab2_layout.setContentsMargins(0, 0, 0, 0)
        self.tab2_layout.setSpacing(0)

        self.temp1 = QLabel("option1")
        self.temp2 = QLabel("option2")
        self.temp3 = QLabel("option3")
        self.temp4 = QLabel("option4")

        self.tab1_layout.addWidget(self.temp1)
        self.tab1_layout.addWidget(self.temp3)
        self.tab1_layout.addWidget(self.temp4)
        self.tab2_layout.addWidget(self.temp1)
        self.tab2_layout.addWidget(self.temp4)
        self.tab2_layout.addWidget(self.temp2)

        self.parameterTabs.addTab(self.tab1, "Test1")
        self.parameterTabs.addTab(self.tab2, "Test2")

        self.layout.addWidget(self.parameterTabs)


class oldConsoleLogFrame(QWidget):
    def __init__(self, parent=None):
        super(oldConsoleLogFrame, self).__init__(parent)
        self.resize(800, 120)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.horizontalScrollBar().setEnabled(False)
        self.scroll_area.setGeometry(self.geometry())
        self.text = QTextEdit()
        self.text.resize(self.geometry().width()-4, self.geometry().height()-1)
        self.text.setReadOnly(True)
        self.scroll_area.setWidget(self.text)

    def log(self, text):
        self.text.append(text)


class OldMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.frame = QFrame(self)
        file_bar = self.menuBar().addMenu("Files")
        file_bar.addAction("Open Video")
        file_bar.addAction("Open Treatment Chain")

        self.resize(800, 680)

        self.video_frame = oldMainFrame(self)
        self.video_frame.setGeometry(0, 25, 640, 530)
        self.parameter_frame = oldParameterFrame(self)
        self.parameter_frame.setGeometry(640, 25, 200, 530)
        self.consolelog_frame = oldConsoleLogFrame(self)
        self.consolelog_frame.move(0, 555)

        self.setCentralWidget(self.frame)


class MediaPlayer(QWidget):
    def __init__(self, parent=None):
        super(MediaPlayer, self).__init__(parent)

        self.setGeometry(0, 0, 640, 480)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.videoWidget = QVideoWidget(self)
        self.videoWidget.setGeometry(0, 0, 640, 480)
        self.setStyleSheet("border: 1px solid;")
        p = self.videoWidget.palette()
        p.setColor(self.videoWidget.backgroundRole(), Qt.black)
        self.videoWidget.setPalette(p)

        # Control Bar Elements
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.set_position)

        self.error = QLabel()
        self.error.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.controlPanel = QFrame(self)
        self.controlPanel.setGeometry(QRect(0, self.height() - 24, self.width(), 24))
        self.controlLayout = QHBoxLayout()
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.positionSlider)
        self.controlPanel.setLayout(self.controlLayout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.media_state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.error.connect(self.handle_error)

    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                                                  QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    @staticmethod
    def exit_call():
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def media_state_changed(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.positionSlider.setValue(position)

    def duration_changed(self, duration):
        self.positionSlider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.set_position(position)

    def handle_error(self):
        self.playButton.setEnabled(False)
        self.error.setText("Error: " + self.mediaPlayer.errorString())


class VideoFrame(QWidget):
    def __init__(self, parent=None):
        super(VideoFrame, self).__init__(parent)

        self.mediaPlayer = MediaPlayer(self)


class ParametersFrame(QWidget):
    def __init__(self, parent=None):
        super(ParametersFrame, self).__init__(parent)

        self.tabs = QTabWidget(self)

        self.tab1 = QFrame(self.tabs)
        self.tab2 = QFrame(self.tabs)
        self.tab1_layout = QVBoxLayout()
        self.tab2_layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1_layout)
        self.tab2.setLayout(self.tab2_layout)
        self.tab1_layout.setContentsMargins(0, 0, 0, 0)
        self.tab1_layout.setSpacing(0)
        self.tab2_layout.setContentsMargins(0, 0, 0, 0)
        self.tab2_layout.setSpacing(0)

        self.temp1 = QLabel("test1")
        self.temp2 = QLabel("test2")
        self.temp3 = QLabel("test3")
        self.temp4 = QLabel("test4")
        self.temp5 = QLabel("test5")
        self.temp6 = QLabel("test6")
        self.temp7 = QLabel("test7")
        self.temp8 = QLabel("test8")

        self.tab1_layout.addWidget(self.temp1)
        self.tab1_layout.addWidget(self.temp2)
        self.tab1_layout.addWidget(self.temp3)
        self.tab2_layout.addWidget(self.temp4)
        self.tab2_layout.addWidget(self.temp5)
        self.tab2_layout.addWidget(self.temp6)
        self.tab2_layout.addWidget(self.temp7)
        self.tab2_layout.addWidget(self.temp8)


class Processus(QWidget):
    def __init__(self, parent=None):
        super(Processus, self).__init__(parent)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.name = QLabel("temp")
        self.button = QPushButton(">")
        self.parameterLayout = QVBoxLayout()

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
            item_layout = QHBoxLayout()
            if parameter[1] == "checkbox":
                new_param = QCheckBox(parameter[0])
                item_layout.addWidget(new_param)
            elif parameter[1] == "slider":
                new_param = QSlider(Qt.Orientation.Horizontal)
                item_layout.addWidget(QLabel(parameter[0]))
                item_layout.addWidget(new_param)
            elif parameter[1] == "textinput":
                new_param = QTextEdit()
                item_layout.addWidget(new_param)
            self.parameterLayout.addLayout(item_layout)


class ProcessFrame(QWidget):
    def __init__(self, parent=None):
        super(ProcessFrame, self).__init__(parent)

        # Window init
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        # Temporary
        fileOpenParams = [
            ["temp", "checkbox"],
            ["temp3", "checkbox"],
            ["temp4", "checkbox"],
            ["temp4", "checkbox"],
            ["temp4", "checkbox"],
            ["temp4", "checkbox"],
            ["temp4", "checkbox"],
            ["temp4", "checkbox"],
            ["temp4", "checkbox"],
            ["temp5", "slider"]
        ]

        # Initialising all modules
        self.fileProcess = Processus(self)
        self.trackProcess = Processus(self)
        self.trajProcess = Processus(self)
        self.fileProcess.init_values("Load Video", parent.videoFrame.mediaPlayer.open_file, fileOpenParams)
        self.trackProcess.init_values("Track", detect, [])
        self.trajProcess.init_values("Extract Trajectory", extract, [])

        self.layout.addWidget(self.fileProcess)
        self.layout.addWidget(self.trackProcess)
        self.layout.addWidget(self.trajProcess)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Window init
        self.resize(894, 659)

        # Frames
        self.videoFrame = VideoFrame(self)
        self.parametersFrame = ParametersFrame(self)
        self.processFrame = ProcessFrame(self)
        self.videoFrame.setGeometry(15, 40, 640, 480)
        self.parametersFrame.setGeometry(670, 40, 209, 480)
        self.processFrame.setGeometry(15, 536, 864, 100)

        # Menus
        # self.menu_files = self.menuBar().addMenu("Files")
        # self.menu_files.addAction("Open Video")
        self.toolbar = QToolBar("test")
        self.addToolBar(self.toolbar)

        openfile_action = QAction("Open File", self)
        openfile_action.triggered.connect(self.videoFrame.mediaPlayer.open_file)
        self.toolbar.addAction(openfile_action)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Application")
    window.show()
    sys.exit(app.exec_())
