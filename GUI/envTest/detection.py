from ultralytics import YOLO
import numpy as np
import math

import sys
sys.path.insert(0, "../External Repositories/sort")
from sort import Sort


def detect(frames, progress_tracker=None):
    print("DETECTING")
    model = YOLO(r'C:\Users\invite\Downloads\train259\weights\best.pt')
    tracker = Sort()
    result = []

    # Longest side, modulo 32 for YOLOv8
    if frames[0].shape[0] > frames[0].shape[1]:
        size = math.floor(frames[0].shape[0] / 32) * 32
    else:
        size = math.floor(frames[0].shape[1] / 32) * 32
    print("TESTING1")
    for frame in frames:
        print("TESTING2")
        objects = model.predict(frame, imgsz=size, conf=0.3)
        print("TESTING3")
        detections = []
        for obj in objects:
            for i, box in enumerate(obj.boxes.xywh):

                # calculate x1 y1 x2 y2
                x, y, w, h = np.array(box.tolist()).astype(int)
                w = int(math.ceil(w/2))
                h = int(math.ceil(h/2))
                detections.append([x - w, y - h, x + w, y + h, 1.0])
        temp = tracker.update(detections)
        print(temp)
        result.append(temp)
        if progress_tracker is not None:
            progress_tracker.set_progress(frame/len(frames))

    return result

# import cv2
# video_path = r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\footage_video\CoreView_178_Core2 05004035 3-4.mp4"
# cap = cv2.VideoCapture(video_path)
# ret, img = cap.read()
# frames = []
# counter = 200
# while ret and counter >= 0:
#     counter -= 1
#     frames.append(img)
#     ret, img = cap.read()
# result = detect(frames)
#
# endframe = []
# for i, frame in enumerate(frames):
#     for obj in result[i]:
#         cv2.circle(frame, (int(obj[0]), int(obj[1])), radius=0, color=(0, 0, 255), thickness=2)
#     endframe.append(frame)
# video_path = 'tempTest.avi'
# size = frames[0].shape[1], frames[0].shape[0]
# video = cv2.VideoWriter(video_path,cv2.VideoWriter_fourcc(*'DIVX'), 25, size)
# for frame in frames:
#     video.write(frame)
# cv2.destroyAllWindows()
# video.release()
#