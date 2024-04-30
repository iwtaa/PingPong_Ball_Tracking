from ultralytics import YOLO

model = YOLO('./yolov8n.pt')

results = model.train(data='D:\\Dataset\\ping-pong-ball.yolov8\\data.yaml', epochs=1)
#model.train(data='ImageNet.yaml', epochs=2, imgsz=220, classes=722)