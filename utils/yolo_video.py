from ultralytics import YOLO
import cv2
import numpy as np

#video
cap = cv2.VideoCapture("../footage_video/CoreView_178_Core2 05004035 3-4.mp4")
facteur = 2

if cap is None:
    print("Video is unreachable. Make sure to enter a valid path.")
    exit(0)

while True:
    ret,img = cap.read()
    img = cv2.resize(img, (img.shape[1]*facteur, img.shape[0]*facteur), img, cv2.INTER_CUBIC)
    model = YOLO('../yolov8n.pt')
    objects = model.predict(img, imgsz=640, conf=0.3)
    for obj in objects:
        for i, box in enumerate(obj.boxes.xywh):
            x, y, w, h = np.array(box.tolist()).astype(int)
            w = min(w, img.shape[1] - x)
            h = min(h, img.shape[0] - y)
            cv2.rectangle(img, (int(x-w/2), int(y-h/2)), (int(x + w/2), int(y + h/2)), color=(255, 0, 0))
    cv2.imshow("temp", img)
    if cv2.waitKey(10) == 27:
        break