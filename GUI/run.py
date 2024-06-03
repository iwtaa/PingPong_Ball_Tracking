import sys

from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import cv2
import numpy as np
from matplotlib import cm

from mpl_toolkits.mplot3d import Axes3D

sys.path.insert(1, '/envTest')
from envTest.detection import detect
from envTest.extract import extract

import time


data = {}


class MediaPlayer(QtCore.QThread):
    frames = []
    frame = 0
    paused = True
    pixmapChange = QtCore.pyqtSignal(QtGui.QPixmap)

    def __init__(self, frame_next_signal, frame_back_signal, pause_signal, fig, ax, parent=None):
        super(MediaPlayer, self).__init__(parent)
        frame_next_signal.connect(self.frame_next)
        frame_back_signal.connect(self.frame_back)
        pause_signal.connect(self.pause)
        self.fig = fig
        self.ax = ax

    def run(self):
        while True:
            self.play()

    def play(self):
        if not self.paused:
            self.setFrame(self.frame + 1)

    def setFrame(self, value):
        if value < 0 or value >= len(self.frames):
            self.pause()
            self.frame = 0
        else:
            self.frame = self.frame + 1
            self.draw_frame()

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
        self.ax.clear()

        # Make data
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.sin(R)
        self.ax.plot_surface(X, Y, Z, vmin=Z.min() * 2, cmap=cm.Blues)

        #plt.ylim(0, 480)
        #plt.xlim(0, 640)
        #plt.gca().invert_yaxis()
        self.ax.set_axis_off()
        self.ax.patch.set_alpha(0.0)
        self.fig.patch.set_alpha(0.0)

        canvas = FigureCanvas(self.fig)
        canvas.draw()
        image = QtGui.QImage(canvas.buffer_rgba(), canvas.size().width(), canvas.size().height(),
                                          QtGui.QImage.Format_ARGB32)
        return QtGui.QPixmap(image)

    def get_frame_pixmap(self):
        return self.convert_nparray_to_QPixmap(self.frames[self.frame]).scaled(640, 480, QtCore.Qt.KeepAspectRatio)

    def draw_frame(self):
        self.pixmapChange.emit(self.join_pixmap(self.get_frame_pixmap(), self.get_fx_pixmap()))

    def convert_nparray_to_QPixmap(self, img):
        h, w, ch = img.shape
        # Convert resulting image to pixmap
        if img.ndim == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        qimg = QtGui.QImage(img.data, w, h, w * ch, QtGui.QImage.Format_BGR888)
        qpixmap = QtGui.QPixmap(qimg)
        return qpixmap

    def join_pixmap(self, p1, p2, mode=QtGui.QPainter.CompositionMode_SourceOver):
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

    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        fig, ax = plt.subplots(figsize=(32, 24), dpi=20, subplot_kw={"projection": "3d"})
        #fig, ax = plt.subplots(figsize=(32, 24), dpi=20)

        self.mediaPlayer = MediaPlayer(self.frame_next_signal, self.frame_back_signal, self.pause_signal, fig, ax, self)
        self.mediaPlayer.pixmapChange.connect(self.set_pixmap)
        self.mediaPlayer.start()

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(0, 0, 640, 480)

    @QtCore.pyqtSlot(QtGui.QPixmap)
    def set_pixmap(self, pixmap):
        self.label.setPixmap(pixmap)

    def open_file(self, value="no value"):
        print(value)
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
                                                            r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\footage_video")
        if fileName != '':
            t = time.time()
            video = cv2.VideoCapture(fileName)
            frames = []
            ret, img = video.read()

            counter = 30
            while ret and counter > 0:
                counter -= 1
                frames.append(img)
                ret, img = video.read()
            print("open_file : ", time.time() - t)
            self.mediaPlayer.set_video(frames)
            return frames
        return None




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


class ProgressTracker:
    progress = 0.0
    state = "waiting"

    def set_progress(self, value):
        self.progress = value
        if self.progress >= 1.0:
            state = "waiting"

    def get_progress(self):
        return self.progress

    def is_progressing(self):
        if self.state == "progressing":
            return True
        else:
            return False

    def start(self):
        self.state = "progressing"
        self.progress = 0.0


class ProcessThread(QtCore.QObject):
    processList = []
    progress_tracker = ProgressTracker()

    def run(self):
        while True:
            if not self.progress_tracker.is_progressing():
                self.progress_tracker.start()

    def add_processes(self, processes):
        for process in processes:
            self.processList.append(process)


class Processus(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Processus, self).__init__(parent)

        self.function = None
        self.parameters = None
        self.return_name = None

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

    def init_values(self, name, function, parameters, settings, return_name):
        self.name.setText(name)
        self.function = function
        self.parameters = parameters
        self.return_name = return_name
        self.button.clicked.connect(self.start)

        for setting in settings:
            item_layout = QtWidgets.QHBoxLayout()
            if setting[1] == "checkbox":
                new_param = QtWidgets.QCheckBox(setting[0])
                item_layout.addWidget(new_param)
            elif setting[1] == "slider":
                new_param = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
                item_layout.addWidget(QtWidgets.QLabel(setting[0]))
                item_layout.addWidget(new_param)
            elif setting[1] == "textinput":
                new_param = QtWidgets.QTextEdit()
                item_layout.addWidget(new_param)
            self.parameterLayout.addLayout(item_layout)

    def start(self):
        params = []
        for parameter in self.parameters:
            if parameter not in data:
                print("Function doesn't have all nescessary parameters to work")
                return
            params.append(data[parameter])
        data[self.return_name] = self.function(*params)


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
        data["tempparam"] = "testingparameters"
        # Initialising all modules
        self.fileProcess = Processus(self)
        self.trackProcess = Processus(self)
        self.trajProcess = Processus(self)
        self.fileProcess.init_values("Load Video", parent.videoFrame.open_file, ["tempparam"], fileOpenParams, "frames")
        self.trackProcess.init_values("Track", detect, ["frames"], [], "detects")
        self.trajProcess.init_values("Extract Trajectory", extract, [], [], "")

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
        self.videoFrame = VideoPlayer(self)
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
            print("testing")
            self.videoFrame.frame_back_signal.emit()
        elif e.key() == QtCore.Qt.Key_F:
            print("testing2")
            self.videoFrame.frame_next_signal.emit()


if __name__ == "__main__":
    plt.switch_backend('agg')
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Application")
    window.show()
    sys.exit(app.exec_())
