from ultralytics import YOLO

# Load your trained model
# model = YOLO('helmet2.pt')
# model = YOLO('helmet2.pt')
model = YOLO('helmet3.pt')

# Export the model to NCNN format
model.export(format='ncnn')
