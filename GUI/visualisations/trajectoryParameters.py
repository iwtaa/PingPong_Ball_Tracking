from PyQt5 import QtWidgets, QtCore
import sys
sys.path.insert(0, '../')
from parameters import Parameters


class TrajectoryParameters:
    def __init__(self, global_data, parent=None):

        self.global_data = global_data

        self.global_data.data['enable_trajectory_visualisation'] = 0
        self.global_data.data['trajectory_dot_size'] = 50
        self.global_data.data['trajectory_history'] = 0

        tab1 = parent.add_tab('trajectory')

        enable1 = QtWidgets.QCheckBox("enable")
        enable1.stateChanged.connect(self.enable_trajectory)

        history = QtWidgets.QCheckBox("history")
        history.stateChanged.connect(self.enable_history)

        dotsize = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        dotsize.setMinimum(10)
        dotsize.setMaximum(1000)
        dotsize.valueChanged.connect(self.dotsize_change)

        tab1.layout().addWidget(enable1)
        tab1.layout().addWidget(history)
        tab1.layout().addWidget(dotsize)

    def enable_trajectory(self, value):
        self.global_data.data['enable_trajectory_visualisation'] = value

    def enable_history(self, value):
        self.global_data.data['trajectory_history'] = value

    def dotsize_change(self, value):
        self.global_data.data['trajectory_dot_size'] = value