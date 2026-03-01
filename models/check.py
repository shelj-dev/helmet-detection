from ultralytics import YOLO

# model = YOLO("yolov8n.pt")
# model = YOLO("yolo26n.pt")
# model = YOLO("helmetV8.pt")

# model = YOLO("helmet2.pt")
model = YOLO("helmet4.pt")

print(model.names)