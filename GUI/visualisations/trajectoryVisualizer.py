import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtGui


class TrajectoryVisualizer:
    def __init__(self, global_data):
        self.fig, self.ax = plt.subplots(figsize=(32, 24), dpi=20, frameon=False)
        self.ax.axis('off')
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.global_data = global_data

    def apply(self, data, current_frame, upto=-1):
        self.ax.clear()
        xlist = [0, 0, 640, 640]
        ylist = [0, 480, 0, 480]
        if self.global_data.data['trajectory_history'] == 2:
            for frame in data:
                if upto != -1 and upto < frame:
                    break
                for detected_object in data[frame]:
                    x1, y1, x2, y2, object_id = detected_object
                    h = y2 - y1
                    w = int(x2 - x1)
                    y = int(y1 + w / 2)
                    x = int(x1 + h / 2)
                    ho, wo = self.global_data.data['size']
                    xfinal = int(x * 640 / wo)
                    yfinal = int(y * 360 / ho)
                    xlist.append(xfinal)
                    ylist.append(yfinal)
        else:
            for detected_object in data[current_frame]:
                x1, y1, x2, y2, object_id = detected_object
                h = y2 - y1
                w = int(x2 - x1)
                y = int(y1 + w / 2)
                x = int(x1 + h / 2)
                ho, wo = self.global_data.data['size']
                xfinal = int(x * 640 / wo)
                yfinal = int(y * 360 / ho)
                xlist.append(xfinal)
                ylist.append(yfinal)
        X = np.array(xlist)
        Y = np.array(ylist)
        plt.scatter(X, Y, s=self.global_data.data['trajectory_dot_size'], c='cyan')
        plt.ylim(0, 480)
        plt.xlim(0, 640)
        plt.gca().invert_yaxis()
        self.ax.patch.set_alpha(0.0)
        self.fig.patch.set_alpha(0.0)

        canvas = FigureCanvas(self.fig)
        canvas.draw()
        image = QtGui.QImage(canvas.buffer_rgba(), canvas.size().width(), canvas.size().height(),
                             QtGui.QImage.Format_ARGB32)
        return QtGui.QPixmap(image)
