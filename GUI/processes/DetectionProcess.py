from GUI.processus import Processus
from PyQt5 import QtWidgets

from GUI.functions.detection import detect

import json


class ProcessusDetection(Processus):
    def __init__(self, global_params, mediaPlayer, parent=None):
        super(ProcessusDetection, self).__init__(global_params, mediaPlayer, parent)
        self.setName("Detect and track")
        self.addControlButton("save", self.save)
        self.addControlButton("load", self.load)
        self.addParameter("savepath", "text")

        self.global_params.data['detections'] = None

    def start(self):
        self.done = True
        self.global_params.data['detections'] = detect(self.mediaPlayer.frames)
        print(self.global_params.data['detections'])

    def save(self):
        if "detections" not in self.global_params.data:
            print("Detections results aren't loaded")
            return
        result = {}
        for frame in self.global_params.data['detections']:
            for item in self.global_params.data['detections'][frame]:
                x1, y1, x2, y2, item_id = item
                if item_id not in result:
                    result[item_id] = []
                detected = {'frame': frame, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
                result[item_id].append(detected)

        # Serializing json
        json_object = json.dumps(result, indent=4)

        # Writing to sample.json
        with open("saved_data\\tracking\\" + self.savepath.text() + '.json', "w") as outfile:
            outfile.write(json_object)

    def load(self):
        result = {}
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
                                                            r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\GUI\saved_data\tracking")
        if fileName != '':
            with open(fileName) as f:
                d = json.load(f)
                print(d)
                for item in d:
                    for frame in d[item]:
                        if frame['frame'] not in result:
                            result[frame['frame']] = []
                        result[frame['frame']].append([frame['x1'], frame['y1'], frame['x2'], frame['y2'], item])
                self.global_params.data['detections'] = result
