from processus import Processus
import sys
sys.path.append("envTest")

from envTest.detection import detect


class ProcessusDetection(Processus):
    def __init__(self, globaldata, parent=None):
        super(ProcessusDetection, self).__init__(parent)

        self.globaldata = globaldata

        self.layout.addWidget(self.name, 0, 0)
        self.layout.addWidget(self.button, 0, 1)
        self.layout.addLayout(self.parameterLayout, 1, 0, 2, 4)
        self.layout.setColumnStretch(0, 3)
        self.layout.setColumnStretch(1, 1)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 3)

        self.button.clicked.connect(self.start)

    def start(self):
        self.globaldata.data['detections'] = detect(self.globaldata.data['frames'])
