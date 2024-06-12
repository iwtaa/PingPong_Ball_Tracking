from PyQt5 import QtCore, QtWidgets, QtGui
from matplotlib import pyplot as plt
import time
import cv2

from GUI.visualisations.trajectoryVisualizer import TrajectoryVisualizer
from GUI.visualisations.videoVisualizer import VideoVisualizer


class MediaPlayer(QtCore.QThread):
    frames = {}
    frame = 0
    size = ()

    paused = True
    pixmapChange = QtCore.pyqtSignal(QtGui.QPixmap)
    time = 0.0
    outlast = 0.0

    def __init__(self, global_params, frame_next_signal, frame_back_signal, pause_signal, parent=None):
        super(MediaPlayer, self).__init__(parent)
        frame_next_signal.connect(self.frame_next)
        frame_back_signal.connect(self.frame_back)
        pause_signal.connect(self.pause)

        self.global_params = global_params

        self.trajectory_visualizer = TrajectoryVisualizer(self.global_params, self)

        self.time = time.time()

    def draw_frame(self):
        t = time.time()
        temp = []

        temp.append(self.draw_video())
        temp.append(self.trajectory_visualizer.apply(
            {'video_frames': self.frames, 'video_size': self.size, 'video_current_frame': self.frame}))

        result = QtGui.QPixmap()
        result.fill(QtCore.Qt.transparent)
        for item in temp:
            result = self.join_pixmap(result, item)

        self.pixmapChange.emit(result)
        print("Draw Frame : " + str(time.time() - t) + "ms")

    def run(self):
        while True:
            self.play()

    def play(self):
        if self.paused or self.frames is None:
            time.sleep(0.1)
        else:
            self.outlast += (time.time() - self.time) * 60
            self.time = time.time()
            frame_length = 0
            while self.outlast >= 1.0:
                frame_length += 1
                self.outlast -= 1.0
            self.setFrame(self.frame + frame_length)

    def setFrame(self, value):
        if 0 <= value < len(self.frames):
            self.frame = value
            self.draw_frame()
        else:
            self.frame = 0

    def pause(self):
        if self.paused:
            self.time = time.time()
            self.paused = False
        else:
            self.paused = True

    def frame_back(self):
        if self.frames is None:
            return
        self.paused = True
        if self.frame != 0:
            self.setFrame(self.frame - 1)

    def frame_next(self):
        if self.frames is None:
            return
        self.paused = True
        if self.frame != len(self.frames) - 1:
            self.setFrame(self.frame + 1)

    def draw_video(self):
        if self.frames is None or self.global_params.data['video_visualisation'] == 0:
            return None
        return self.convert_nparray_to_QPixmap(self.frames[self.frame]).scaled(640, 480, QtCore.Qt.KeepAspectRatio)

    @staticmethod
    def convert_nparray_to_QPixmap(img):
        h, w, ch = img.shape
        # Convert resulting image to pixmap
        if img.ndim == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        qimg = QtGui.QImage(img.data, w, h, w * ch, QtGui.QImage.Format_BGR888)
        qpixmap = QtGui.QPixmap(qimg)
        return qpixmap

    @staticmethod
    def join_pixmap(p1, p2, mode=QtGui.QPainter.CompositionMode_SourceOver):
        if p2 is None:
            return p1
        s = p1.size().expandedTo(p2.size())
        result = QtGui.QPixmap(s)
        result.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(result)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawPixmap(QtCore.QPoint(), p1)
        painter.setCompositionMode(mode)
        painter.drawPixmap(result.rect(), p2, p2.rect())
        painter.end()
        return result

    def set_video(self, video):
        self.frames = video
        self.paused = True
        self.setFrame(0)


class VideoPlayer(QtWidgets.QWidget):
    frame_next_signal = QtCore.pyqtSignal()
    frame_back_signal = QtCore.pyqtSignal()
    pause_signal = QtCore.pyqtSignal()

    def __init__(self, global_data, parent=None):
        super(VideoPlayer, self).__init__(parent)

        fig, ax = plt.subplots(figsize=(32, 24), dpi=20, frameon=False)
        ax.axis('off')
        ax = fig.add_axes([0, 0, 1, 1])
        self.mediaPlayer = MediaPlayer(global_data, self.frame_next_signal, self.frame_back_signal, self.pause_signal, self)
        self.mediaPlayer.pixmapChange.connect(self.set_pixmap)
        self.mediaPlayer.start()

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(0, 0, 640, 480)

        self.controlBar = QtWidgets.QWidget(self)
        self.controlBar.setLayout(QtWidgets.QHBoxLayout())
        self.controlBar.layout().setAlignment(QtCore.Qt.AlignBottom)

        self.playButton = QtWidgets.QPushButton(">")
        self.nextFrame = QtWidgets.QPushButton("+")
        self.previousFrame = QtWidgets.QPushButton("-")

        self.playButton.clicked.connect(self.mediaPlayer.pause)
        self.nextFrame.clicked.connect(self.mediaPlayer.frame_next)
        self.previousFrame.clicked.connect(self.mediaPlayer.frame_back)

        self.controlBar.layout().addWidget(self.playButton)
        self.controlBar.layout().addWidget(self.nextFrame)
        self.controlBar.layout().addWidget(self.previousFrame)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.controlBar)

    @QtCore.pyqtSlot(QtGui.QPixmap)
    def set_pixmap(self, pixmap):
        self.label.setPixmap(pixmap)

    def open_file(self, value="no value"):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
                                                            r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\footage_video")

        if fileName != '':
            video = cv2.VideoCapture(fileName)
            frames = []
            ret, img = video.read()
            counter = 25
            while ret and counter != 0:
                counter -= 1
                frames.append(img)
                ret, img = video.read()
            self.mediaPlayer.set_video(frames)
            return frames
        return None
