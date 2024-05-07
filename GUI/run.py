import sys
import cv2

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


def loadVideo():
    video = []
    cap = cv2.VideoCapture("C:\\Users\\invite\\PycharmProjects\\PingPong_Ball_Tracking\\footage_video\\CoreView_178_Core2 05004035 3-4.mp4")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        video.append(p)

    return video


class VideoPlayer(QThread):
    changePixmap = pyqtSignal(QImage)
    frame = 0
    video = None

    def init(self, video):
        self.video = video

    def run(self):
        while True:
            self.nextFrame()
            self.changePixmap.emit(self.video[self.frame])

    def nextFrame(self):
        if (self.frame + 1) < len(self.video):
            self.frame += 1
        print("next frame: " + str(self.frame))


class VideoFrame(QWidget):
    def __init__(self, parent=None):
        super(VideoFrame, self).__init__(parent)

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

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget(self)
        videoWidget.setGeometry(0, 50, 640, 480)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.error = QLabel()
        self.error.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        openButton = QPushButton("Open Video", self)
        openButton.setGeometry(QRect(0, 600, 50, 50))
        openButton.setToolTip("Open Video File")
        openButton.setStatusTip("Open Video File")
        openButton.setFixedHeight(24)
        openButton.clicked.connect(self.openFile)

        # Create a widget for window contents
        wid = QWidget(self)
        wid.setGeometry(QRect(0, 50, 620, 480))

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout(self)
        controlLayout.setGeometry(QRect(0, 530, 640, 100))
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        self.mediaPlayer.setVideoOutput(videoWidget)
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


class ParameterFrame(QWidget):
    def __init__(self, parent=None):
        super(ParameterFrame, self).__init__(parent)

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


class ConsoleLogFrame(QWidget):
    def __init__(self, parent=None):
        super(ConsoleLogFrame, self).__init__(parent)
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.frame = QFrame(self)

        self.resize(800, 650)

        self.video_frame = VideoFrame(self)
        self.video_frame.setGeometry(0, 0, 640, 530)
        self.parameter_frame = ParameterFrame(self)
        self.parameter_frame.setGeometry(640, 0, 200, 530)
        self.consolelog_frame = ConsoleLogFrame(self)
        self.consolelog_frame.move(0, 530)

        self.setCentralWidget(self.frame)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Application")
    window.show()
    sys.exit(app.exec_())
