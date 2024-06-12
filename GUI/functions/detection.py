from ultralytics import YOLO
import numpy as np
import math

import sys
sys.path.insert(0, "../External Repositories/sort")
from sort import Sort


def detect(frames, progress_tracker=None):
    model = YOLO(r'C:\Users\invite\Downloads\train259\weights\best.pt')
    tracker = Sort()
    result = {}

    # Longest side, modulo 32 for YOLOv8
    if frames[0].shape[0] > frames[0].shape[1]:
        size = math.floor(frames[0].shape[0] / 32) * 32
    else:
        size = math.floor(frames[0].shape[1] / 32) * 32
    counter = 0
    for frame in frames:
        objects = model.predict(frame, imgsz=size, conf=0.3)
        detections = []
        for obj in objects:
            for i, box in enumerate(obj.boxes.xywh):

                # calculate x1 y1 x2 y2
                x, y, w, h = np.array(box.tolist()).astype(int)
                w = int(math.ceil(w/2))
                h = int(math.ceil(h/2))
                detections.append([x - w, y - h, x + w, y + h, 1.0])
        temp = tracker.update(detections)
        result[counter] = temp
        if progress_tracker is not None:
            progress_tracker.set_progress(frame/len(frames))
        counter += 1

    return result