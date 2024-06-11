from ultralytics import YOLO
import cv2
import numpy as np
import math
import skvideo.io

# import sys
# sys.path.insert(0, "../External Repositories/sort")
# from sort import Sort

# video
cap = cv2.VideoCapture(r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\footage_video\CoreView_178_Core2 05004035 3-4.mp4")
facteur = 1
# tracker = Sort()
# tracking = False
video_output = False


def num_to_rgb(val, max_val=20):
    if val > max_val:
        val = val % max_val
    if val < 0 or max_val < 0:
        raise ValueError("arguments may not be negative")

    i = (val * 255 / max_val);
    r = round(math.sin(0.024 * i + 0) * 127 + 128);
    g = round(math.sin(0.024 * i + 2) * 127 + 128);
    b = round(math.sin(0.024 * i + 4) * 127 + 128);
    return r, g, b


# Detection
if cap is None:
    print("Video is unreachable. Make sure to enter a valid path.")
    exit(0)
ret, img = cap.read()

if img.shape[0] > img.shape[1]:
    size = math.floor(img.shape[0] / 32) * 32
else:
    size = math.floor(img.shape[1] / 32) * 32

object_points = {}
points = []
frames = []
model = YOLO(r'C:\Users\invite\Downloads\train259\weights\best.pt')
#counter = 100
while ret :#and counter != 0:
    #counter -= 1
    #img = img[:640, 1280:, :]
    print(img.shape)
    objects = model.predict(img, imgsz=size, conf=0.05)

    #Affichage du Tracking avec SORT
    # if tracking:
    #     detections = []
    #     for obj in objects:
    #         for i, box in enumerate(obj.boxes.xywh):
    #             # calculate x1 y1 x2 y2
    #             x, y, w, h = np.array(box.tolist()).astype(int)
    #             w = int(math.ceil(w / 2))
    #             h = int(math.ceil(h / 2))
    #             detections.append([x - w, y - h, x + w, y + h, 1.0])
    #     temp = tracker.update(detections)
    #     for item in temp:
    #         x1, y1, x2, y2, item_id = item
    #         if item_id not in object_points:
    #             object_points[item_id] = []
    #         object_points[item_id].append((int(x1 + (x2 - x1) / 2), int(y1 + (y2 - y1) / 2)))
#
    #     for item in object_points:
    #         if len(object_points[item]) <= 4:
    #             continue
    #         for index, point in enumerate(object_points[item]):
    #             cv2.circle(img, point, radius=0, color=num_to_rgb(item), thickness=8)
    #             if index != 0:
    #                 cv2.line(img, point, object_points[item][index-1], color=num_to_rgb(item), thickness=2)
#
    # #Affichage des detections uniquement
    # else:
    for obj in objects:
        for i, box in enumerate(obj.boxes.xywh):
            x, y, w, h = np.array(box.tolist()).astype(int)
            w = min(w, img.shape[1] - x)
            h = min(h, img.shape[0] - y)
            cv2.rectangle(img, (int(x-w/2), int(y-h/2)), (int(x + w/2), int(y + h/2)), color=(0, 0, 255), thickness=2)
            cv2.circle(img, (x, y), radius=0, color=(0, 0, 255), thickness=5)
            points.append((x, y))
    for point in points:
        cv2.circle(img, point, radius=0, color=(0, 0, 255), thickness=8)

    #Creation de la video
    if video_output:
        frames.append(img)
    cv2.imshow("temp", img)
    if cv2.waitKey(1) == 27:
        break
    ret, img = cap.read()

if video_output:
    video_path = 'outputVideo.avi'
    size = frames[0].shape[1], frames[0].shape[0]
    video = cv2.VideoWriter(video_path,cv2.VideoWriter_fourcc(*'DIVX'), 25, size)

    for frame in frames:
        video.write(frame)

    cv2.destroyAllWindows()
    video.release()
