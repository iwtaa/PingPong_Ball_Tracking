from GUI.processus import Processus


class ProcessusOpenFile(Processus):
    def __init__(self, global_params, mediaPlayer, parent=None):
        super(ProcessusOpenFile, self).__init__(global_params, mediaPlayer, parent)
        self.setName("Open Video")

        self.parent = parent

    def start(self):
        self.done = True
        self.mediaPlayer.frames = self.parent.parent.videoFrame.open_file()
        self.mediaPlayer.size = self.mediaPlayer.frames[0].shape[:2]
