from PyQt5 import QtWidgets, QtCore


class Parameters(QtWidgets.QWidget):
    def __init__(self, global_data, parent=None):
        super(Parameters, self).__init__(parent)

        self.global_data = global_data

        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.setGeometry(QtCore.QRect(0, 0, 209, 400))

    def add_tab(self, name):
        tab = QtWidgets.QFrame(self.tabs)
        tab.setGeometry(QtCore.QRect(0, 0, 209, 480))
        tab_layout = QtWidgets.QVBoxLayout()
        tab.setLayout(tab_layout)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)

        self.tabs.addTab(tab, name)
        return tab
