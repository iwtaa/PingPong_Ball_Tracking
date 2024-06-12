import numpy as np
from matplotlib import pyplot as plt
from PyQt5 import QtGui, QtCore
import cv2


class VideoVisualizer:
    def __init__(self, global_params, parent=None):
        self.global_params = global_params

    def apply(self, data):
        if data['video_frames'] is None or self.global_params.data['video_visualisation'] == 0:
            return None
        return self.convert_nparray_to_QPixmap(data['video_frames'][data['video_current_frame']]).scaled(640, 480, QtCore.Qt.KeepAspectRatio)

    @staticmethod
    def convert_nparray_to_QPixmap(img):
        h, w, ch = img.shape
        # Convert resulting image to pixmap
        if img.ndim == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        qimg = QtGui.QImage(img.data, w, h, w * ch, QtGui.QImage.Format_BGR888)
        qpixmap = QtGui.QPixmap(qimg)
        return qpixmap
