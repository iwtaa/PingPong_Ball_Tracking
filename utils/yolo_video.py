from ultralytics import YOLO
import cv2
import numpy as np

#video
cap = cv2.VideoCapture("C:\\Users\\invite\\PycharmProjects\\PingPong_Ball_Tracking\\footage_video\\CoreView_178_Core2 05004035 3-4.mp4")
facteur = 2

#Detection

if cap is None:
    print("Video is unreachable. Make sure to enter a valid path.")
    exit(0)
ret,img = cap.read()
while ret:
    print(ret)
    model = YOLO('C:\\Users\\invite\\PycharmProjects\\PingPong_Ball_Tracking\\External Repositories\\best.pt')
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
    ret, img = cap.read()