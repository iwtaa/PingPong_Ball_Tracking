from ultralytics import YOLO
import cv2
import numpy as np
import math
import skvideo.io

# video
cap = cv2.VideoCapture(r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\footage_video\CoreView_178_Core2 05004035 3-4.mp4")
facteur = 1

# Detection
if cap is None:
    print("Video is unreachable. Make sure to enter a valid path.")
    exit(0)
ret, img = cap.read()

if img.shape[0] > img.shape[1]:
    size = math.floor(img.shape[0] / 32) * 32
else:
    size = math.floor(img.shape[1] / 32) * 32

points = []
frames = []

while ret:
    model = YOLO(r'C:\Users\invite\Downloads\train259\weights\best.pt')
    objects = model.predict(img, imgsz=size, conf=0.3)
    for obj in objects:
        for i, box in enumerate(obj.boxes.xywh):
            x, y, w, h = np.array(box.tolist()).astype(int)
            w = min(w, img.shape[1] - x)
            h = min(h, img.shape[0] - y)
            cv2.rectangle(img, (int(x-w/2), int(y-h/2)), (int(x + w/2), int(y + h/2)), color=(0, 0, 255), thickness=2)
            points.append((x, y))
            for point in points:
                cv2.circle(img, point, radius=0, color=(0, 0, 255), thickness=2)
    frames.append(img)
    # cv2.imshow("temp", img)
    if cv2.waitKey(1) == 27:
        break
    ret, img = cap.read()

video_path = 'outputVideo.avi'
size = frames[0].shape[1], frames[0].shape[0]
video = cv2.VideoWriter(video_path,cv2.VideoWriter_fourcc(*'DIVX'), 25, size)

for frame in frames:
    video.write(frame)

cv2.destroyAllWindows()
video.release()
