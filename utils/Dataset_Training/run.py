from ultralytics import YOLO

model = YOLO('./yolov8n.pt')

results = model.train(data='D:\\Dataset\\ping-pong-ball.yolov8\\data.yaml', epochs=1, single_cls=True, box=10.0, cls=0.0, dfl=0.0, pose=0.0, plots=True)
#model.train(data='ImageNet.yaml', epochs=2, imgsz=220, classes=722)