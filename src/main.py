# Here we will combine all the pipelines and run them in a sequence
from models.detectionModel import DetectionModel

# Initialize
model = DetectionModel()
results = model.detect('./src/models/download.jpg')

print(results)