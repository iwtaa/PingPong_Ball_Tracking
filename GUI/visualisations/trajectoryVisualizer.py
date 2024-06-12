import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtGui, QtCore


class TrajectoryVisualizer:
    def __init__(self, global_params, parent=None):
        self.fig, self.ax = plt.subplots(figsize=(32, 24), dpi=20, frameon=False)
        self.ax.axis('off')
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.global_params = global_params

    def apply(self, data):
        if self.global_params.data['trajectory_visualisation'] == 0 or self.global_params.data['detections'] is None:
            return None

        self.ax.clear()
        xlist = []
        ylist = []

        if self.global_params.data['trajectory_history'] == 2:
            for frame in self.global_params.data['detections']:
                if frame > data['video_current_frame']:
                    break
                for detected_object in self.global_params.data['detections'][frame]:
                    x, y = self.object_to_point(detected_object, data['video_size'])
                    xlist.append(x)
                    ylist.append(y)
        else:
            for detected_object in self.global_params.data['detections'][data['video_current_frame']]:
                x, y = self.object_to_point(detected_object, data['video_size'])
                xlist.append(x)
                ylist.append(y)
        X = np.array(xlist)
        Y = np.array(ylist)
        plt.scatter(X, Y, s=self.global_params.data['trajectory_dot_size'], color=(0, 0, 1))
        plt.ylim(0, 480)
        plt.xlim(0, 640)
        plt.gca().invert_yaxis()
        self.ax.patch.set_alpha(0.0)
        self.fig.patch.set_alpha(0.0)

        canvas = FigureCanvas(self.fig)
        canvas.draw()
        image = QtGui.QImage(canvas.buffer_rgba(), canvas.size().width(), canvas.size().height(),
                             QtGui.QImage.Format_ARGB32)
        return QtGui.QPixmap(image).scaled(640, 480, QtCore.Qt.KeepAspectRatio)

    @staticmethod
    def object_to_point(object, size):
        x1, y1, x2, y2, object_id = object
        h = y2 - y1
        w = int(x2 - x1)
        y = int(y1 + w / 2)
        x = int(x1 + h / 2)
        ho, wo = size
        xfinal = int(x * 640 / wo)
        yfinal = int(y * 360 / ho)
        return xfinal, yfinal
