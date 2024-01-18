# Here we will combine all the pipelines and run them in a sequence
from classes.detectionModel import DetectionModel

# Initialize
model = DetectionModel()
results = model.detect('./tests/download.jpg')

print(results)