import threading
import cv2
import torch
from classes.depth_camera import DepthCamera
from classes.yolo_model import YoloModel
from ultralytics import solutions

def detect_objects(cam, model, counter):
    while True:
        image, depth, depth_colormap = cam.get_image_data()
        
        # Ensure the image is in RGB format and resized to 640x640
        # if image.shape[2] == 1:
        #     image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        # elif image.shape[2] == 4:
        #     image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        # else:
        #     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # image = cv2.resize(image, (640, 640))
        
        # Convert the image to a tensor and normalize
        # image_tensor = torch.tensor(image).float().permute(2, 0, 1).unsqueeze(0) / 255.0
        # image_tensor = image_tensor.to(model.device)
        # print(image_tensor.shape)
        
        # Perform detection
        results = model.track(image)
        print(results)
        # print(results)
        image_with_detections = counter.start_counting(image, results)
        # Draw detections
        # image_with_detections = model.draw_detections(image, results)
        
        # Display the images
        cv2.imshow('Color Image', image_with_detections)
        
        # Check for user input to close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close all windows
    cv2.destroyAllWindows()
    cam.stop()

def main():
    # Initialize camera and model
    cam = DepthCamera()
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = YoloModel('../weights/yolov8n.pt', device=device)
    counter = solutions.ObjectCounter(
        classes_names=model.model.names,
        reg_pts=[(0,0), (0, 480), (640, 480), (640, 0)],
        line_thickness=1,
        region_thickness=2
        )
    
    print("Init done")
    
    # Create and start the detection thread
    detection_thread = threading.Thread(target=detect_objects, args=(cam, model, counter))
    detection_thread.start()
    
    # Join the thread to wait for its completion
    detection_thread.join()

if __name__ == "__main__":
    main()
