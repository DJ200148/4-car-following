from ultralytics import YOLO
import cv2
import numpy as np
import os

class DetectionModel:
    def __init__(self, model_name='yolov8m.pt'):
        self.model = YOLO(model_name)

    def detect(self, image):
        results = self.model(image)
        return results

    def draw_detections(self, results):
        # Ensure the image is a NumPy array in the correct format
        image = np.array(results.orig_img)
        if image.ndim == 2 or image.shape[2] == 1:
            # Convert grayscale to BGR format
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        # Extract bounding boxes, classes, names, and confidences
        boxes = results.boxes.xyxy.tolist()
        classes = results.boxes.cls.tolist()
        names = results.names
        confidences = results.boxes.conf.tolist()

        # Iterate through the results
        for box, cls, conf in zip(boxes, classes, confidences):
            x1, y1, x2, y2 = map(int, box)
            confidence = conf
            detected_class = cls
            name = names[int(cls)]
            label = f'{name} {confidence:.2f}'
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        return image
    
    def save_results(self, image, filepath):
        # Save the image
        cv2.imwrite(filepath, image)
    
    
    # Extra methods
    def save_model(self, filepath):
        self.model.save(filepath)

    def load_model(self, filepath):
        self.model.load(filepath)
        
    def detect_real_time(self, source=0):
        cap = cv2.VideoCapture(source)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = self.detect(frame)
            frame = self.draw_detections(frame, results)
            cv2.imshow('Real-time Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()