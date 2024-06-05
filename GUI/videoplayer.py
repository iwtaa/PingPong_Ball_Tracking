from PyQt5 import QtCore, QtWidgets, QtGui
from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
import time
import numpy as np
import cv2

from trajectoryVisualizer import TrajectoryVisualizer


class MediaPlayer(QtCore.QThread):
    frames = []
    frame = 0
    paused = True
    pixmapChange = QtCore.pyqtSignal(QtGui.QPixmap)

    def __init__(self, global_data, frame_next_signal, frame_back_signal, pause_signal, parent=None):
        super(MediaPlayer, self).__init__(parent)
        frame_next_signal.connect(self.frame_next)
        frame_back_signal.connect(self.frame_back)
        pause_signal.connect(self.pause)
        self.trajectory_visualizer = TrajectoryVisualizer(global_data)
        self.global_data = global_data

    def run(self):
        while True:
            self.play()

    def play(self):
        if self.paused:
            time.sleep(0.3)
        else:
            self.setFrame(self.frame + 1)

    def setFrame(self, value):
        if 0 <= value < len(self.frames):
            self.frame = self.frame + 1
            self.draw_frame()
        else:
            self.pause()
            self.frame = 0

    def pause(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def frame_back(self):
        self.paused = True
        if self.frame != 0:
            self.setFrame(self.frame - 1)

    def frame_next(self):
        self.paused = True
        if self.frame != len(self.frames) - 1:
            self.setFrame(self.frame + 1)

    def get_fx_pixmap(self):
        if "detections" in self.global_data.data:
            return self.trajectory_visualizer.apply(self.global_data.data['detections'])
        else:
            return None

    def get_frame_pixmap(self):
        return self.convert_nparray_to_QPixmap(self.frames[self.frame]).scaled(640, 480, QtCore.Qt.KeepAspectRatio)

    def draw_frame(self):
        self.pixmapChange.emit(self.join_pixmap(self.get_frame_pixmap(), self.get_fx_pixmap()))

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

    @QtCore.pyqtSlot(QtGui.QPixmap)
    def set_pixmap(self, pixmap):
        self.label.setPixmap(pixmap)

    def open_file(self, value="no value"):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
                                                            r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\footage_video")
        if fileName != '':
            t = time.time()
            video = cv2.VideoCapture(fileName)
            frames = []
            ret, img = video.read()

            counter = 10
            while ret and counter > 0:
                counter -= 1
                frames.append(img)
                ret, img = video.read()
            print("open_file : ", time.time() - t)
            self.mediaPlayer.set_video(frames)
            return frames
        return None
