from processus import Processus
from PyQt5 import QtWidgets
import sys
sys.path.append("../envTest")

from envTest.detection import detect

import json


class ProcessusDetection(Processus):
    def __init__(self, globaldata, parent=None):
        super(ProcessusDetection, self).__init__(parent)
        self.setName("Detect")
        self.addControlButton("save", self.save)
        self.addControlButton("load", self.load)
        self.globaldata = globaldata
        self.addParameter("testing", "checkbox")
        self.addParameter("savepath", "text")

    def start(self):
        self.done = True
        self.globaldata.data['detections'] = detect(self.globaldata.data['frames'])
        print(self.globaldata.data['detections'])

    def save(self):
        if "detections" not in self.globaldata.data:
            print("Detections results aren't loaded")
            return
        result = {}
        for frame in self.globaldata.data['detections']:
            for item in self.globaldata.data['detections'][frame]:
                x1, y1, x2, y2, item_id = item
                if item_id not in result:
                    result[item_id] = []
                detected = {'frame': frame, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
                result[item_id].append(detected)

        # Serializing json
        json_object = json.dumps(result, indent=4)

        # Writing to sample.json
        with open("saved_data\\" + self.savepath.text() + '.json', "w") as outfile:
            outfile.write(json_object)

    def load(self):
        result = {}
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
                                                            r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\GUI\saved_data")
        if fileName != '':
            with open(fileName) as f:
                d = json.load(f)
                print(d)
                for item in d:
                    for frame in d[item]:
                        if frame['frame'] not in result:
                            result[frame['frame']] = []
                        result[frame['frame']].append([frame['x1'], frame['y1'], frame['x2'], frame['y2'], item])
                self.globaldata.data['detections'] = result

