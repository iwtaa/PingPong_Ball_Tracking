from processus import Processus


class ProcessusOpenFile(Processus):
    def __init__(self, globalData, parent=None):
        super(ProcessusOpenFile, self).__init__(parent)

        self.globalData = globalData

        self.parent = parent

        self.layout.addWidget(self.name, 0, 0)
        self.layout.addWidget(self.button, 0, 1)
        self.layout.addLayout(self.parameterLayout, 1, 0, 2, 4)
        self.layout.setColumnStretch(0, 3)
        self.layout.setColumnStretch(1, 1)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 3)

        self.button.clicked.connect(self.start)

    def start(self):
        self.globalData.data['frames'] = self.parent.parent.videoFrame.open_file()
        self.globalData.data['size'] = self.globalData.data['frames'][0].shape[:2]
