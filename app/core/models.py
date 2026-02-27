from ultralytics import YOLO


model_detection = YOLO("models/helmetV8.pt", task="detect")