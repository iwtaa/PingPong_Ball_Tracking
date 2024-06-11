from ultralytics import YOLO

model = YOLO('./yolov8n.pt')
dataset_path = r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\utils\Dataset_images\imagenet-1k_tennis-table-ball.v1i.yolov8\data.yaml"

model.train(data=dataset_path, epochs=1, augment=True, single_cls=True, box=10.0, cls=0.0, dfl=0.0, pose=0.0, plots=True)