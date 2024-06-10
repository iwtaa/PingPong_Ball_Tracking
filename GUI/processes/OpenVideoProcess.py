from processus import Processus


class ProcessusOpenFile(Processus):
    def __init__(self, globalData, parent=None):
        super(ProcessusOpenFile, self).__init__(parent)
        self.setName("Open Video")

        self.globalData = globalData

        self.parent = parent

    def start(self):
        self.done = True
        self.globalData.data['frames'] = self.parent.parent.videoFrame.open_file()
        self.globalData.data['size'] = self.globalData.data['frames'][0].shape[:2]
