from PyQt5 import QtWidgets, QtCore


class Processus(QtWidgets.QWidget):
    def __init__(self, global_params, mediaPlayer, parent=None):
        super(Processus, self).__init__(parent)

        self.done = False
        self.setInitialLayout()

        self.global_params = global_params
        self.mediaPlayer = mediaPlayer

        self.is_local = True

        self.button.clicked.connect(self.start)

    def addControlButton(self, name, function):
        element = QtWidgets.QPushButton(name)
        self.controlLayout.addWidget(element)
        element.clicked.connect(function)

    def addParameter(self, name, type):
        if type == "checkbox":
            element = QtWidgets.QCheckBox(name)
            temp = QtWidgets.QHBoxLayout()
            temp.setAlignment(QtCore.Qt.AlignHCenter)
            temp.addWidget(element)
            self.layout().addLayout(temp)
        elif type == "text":
            label = QtWidgets.QLabel(name)
            self.savepath = QtWidgets.QLineEdit()
            temp = QtWidgets.QHBoxLayout()
            temp.setAlignment(QtCore.Qt.AlignHCenter)
            temp.addWidget(label)
            temp.addWidget(self.savepath)
            self.layout().addLayout(temp)

    def setName(self, name):
        self.name.setText(name)

    def setInitialLayout(self):
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.controlLayout = QtWidgets.QHBoxLayout()

        self.name = QtWidgets.QLabel("temp")
        self.name.setAlignment(QtCore.Qt.AlignHCenter)
        self.button = QtWidgets.QPushButton(">")
        self.layout().addWidget(self.name)
        self.controlLayout.addWidget(self.button)
        self.layout().addLayout(self.controlLayout)

