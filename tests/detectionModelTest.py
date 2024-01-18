import sys
import os
current_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(current_directory, '../src'))
sys.path.append(parent_directory)

from models.detectionModel import DetectionModel

# Initialize
model = DetectionModel()
results = model.detect('./tests/download.jpg')
# print(results)
new_image = model.draw_detections(results[0])

model.save_results(new_image, './tests/results.jpg')

print(results)