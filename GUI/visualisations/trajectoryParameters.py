from PyQt5 import QtWidgets, QtCore
import sys
sys.path.insert(0, '../')
from parameters import Parameters


class TrajectoryParameters:
    def __init__(self, global_params, parent=None):

        self.global_params = global_params

        self.global_params.data['trajectory_visualisation'] = 0
        self.global_params.data['trajectory_dot_size'] = 50
        self.global_params.data['trajectory_history'] = 0
        self.global_params.data['trajectory_decay'] = 10

        tab1 = parent.add_tab('trajectory')

        enabled = QtWidgets.QCheckBox("enable")
        enabled.stateChanged.connect(self.enable_trajectory)

        history = QtWidgets.QCheckBox("history")
        history.stateChanged.connect(self.enable_history)

        dotsize = QtWidgets.QHBoxLayout()
        dotsize_label = QtWidgets.QLabel("Dot Size")
        dotsize_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        dotsize_slider.setMinimum(10)
        dotsize_slider.setMaximum(1000)
        dotsize_slider.valueChanged.connect(self.dotsize_change)
        dotsize.addWidget(dotsize_label)
        dotsize.addWidget(dotsize_slider)

        color = QtWidgets.QHBoxLayout()
        color_r_label = QtWidgets.QLabel("COLOR: r")
        color_r = QtWidgets.QLineEdit()
        color_r_label = QtWidgets.QLabel("g")
        color_r_label = QtWidgets.QLabel("b")

        tab1.layout().addWidget(enabled)
        tab1.layout().addWidget(history)
        tab1.layout().addLayout(dotsize)

    def enable_trajectory(self, value):
        self.global_params.data['trajectory_visualisation'] = value

    def enable_history(self, value):
        self.global_params.data['trajectory_history'] = value

    def dotsize_change(self, value):
        self.global_params.data['trajectory_dot_size'] = value
