from ultralytics import YOLO
import cv2
import numpy as np

img = cv2.imread('C:\\Users\\invite\\PycharmProjects\\PingPong_Ball_Tracking\\utils\\Dataset_Training\\table tennis.v11i.yolov8\\valid\\images\\frames-project00281_png.rf.3903d218fb726a59a3272983d0f19241.jpg')
facteur = 1

if img is None:
    print("Image is unreachable. Make sure to enter a valid path.")
    exit(0)
img = cv2.resize(img, (img.shape[1]*facteur, img.shape[0]*facteur), img, cv2.INTER_CUBIC)
model = YOLO('C:\\Users\\invite\\PycharmProjects\\PingPong_Ball_Tracking\\utils\\runs\\detect\\train4\\weights\\best.pt')
objects = model.predict(img, imgsz=640, conf=0.3)
for obj in objects:
    for i, box in enumerate(obj.boxes.xywh):
        x, y, w, h = np.array(box.tolist()).astype(int)
        w = min(w, img.shape[1] - x)
        h = min(h, img.shape[0] - y)
        cv2.rectangle(img, (int(x-w/2), int(y-h/2)), (int(x + w/2), int(y + h/2)), color=(255, 0, 0))
while True:
    cv2.imshow("temp", img)
    if cv2.waitKey(10) == 27:
        break