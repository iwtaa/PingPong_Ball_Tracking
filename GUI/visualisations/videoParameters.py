from PyQt5 import QtWidgets, QtCore
import sys
sys.path.insert(0, '../')
from parameters import Parameters


class VideoParameters:
    def __init__(self, global_params, parent=None):

        self.global_params = global_params

        self.global_params.data['video_visualisation'] = 0
        self.global_params.data['video_speed'] = 50

        tab1 = parent.add_tab('video')

        enable = QtWidgets.QCheckBox("enable")
        enable.stateChanged.connect(self.enable_video)

        speed = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        speed.setMinimum(1)
        speed.setMaximum(60)
        speed.valueChanged.connect(self.speed_change)

        tab1.layout().addWidget(enable)
        tab1.layout().addWidget(speed)


    def enable_video(self, value):
        self.global_params.data['video_visualisation'] = value

    def speed_change(self, value):
        self.global_params.data['video_speed'] = value
