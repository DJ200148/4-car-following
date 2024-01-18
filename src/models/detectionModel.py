from ultralytics import YOLO

# Initialize
model = YOLO('yolov8m.pt')

# Perform detection
results = model('./src/models/download.jpg')

print(results)

class DetectionModel:
    def __init__(self, model_name = 'yolov8m.pt'):
        self.model = YOLO(model_name)

    def detect(self, image):
        results = self.model(image)
        return results