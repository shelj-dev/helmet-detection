from ultralytics import YOLO

# model = YOLO("yolov8n.pt")
# model = YOLO("yolo26n.pt")
# model = YOLO("helmetV8.pt")

# model = YOLO("helmet2.pt")
model = YOLO("best (1).pt")

print(model.names)