from ultralytics import YOLO

model = YOLO('./yolov8n.pt')
dataset_path = r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\utils\Dataset_images\imagenet-1k_tennis-table-ball.v1i.yolov8\data.yaml"

model.tune(data=dataset_path, epochs=30, iterations=300, plots=False, save=False, val=False)
