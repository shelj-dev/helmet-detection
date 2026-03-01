from ultralytics import YOLO


import torch
# model = torch.load('helment_no_helmet98.6.pth')
# model.eval()
# Use for inference on images

# model_detection = YOLO("models/helmetV8.pt", task="detect")


# model_detection = YOLO("models/helmetV8_ncnn_model", task="detect")
# model_detection = YOLO("models/yolov8n_ncnn_model", task="detect")
# model_detection = YOLO("models/Helmet_Detection_Models", task="detect")

# model_detection = YOLO("models/helmet.pt", task="detect")

# model_detection = YOLO("models/helmet_ncnn_model", task="detect")

###################
model_detection = YOLO("models/helmet1_ncnn_model", task="detect")
###################

# model_detection = YOLO("models/helmet2_ncnn_model", task="detect")
# model_detection = YOLO("models/helmet4_ncnn_model", task="detect")
# model_detection = torch.load("models/helmet5.pth", task="detect")
