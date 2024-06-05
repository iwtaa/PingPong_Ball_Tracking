from PyQt5 import QtWidgets


class Processus(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Processus, self).__init__(parent)

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
        self.is_local = True

