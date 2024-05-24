from classes.depth_camera import DepthCamera
import cv2
from classes.yolo_model import YoloModel
import torch


cam = DepthCamera()
model = YoloModel('../weights/yolov8n.pt', device='cuda')

print("Init done")

while True:
    image, depth, depth_colormap = cam.get_image_data()
    # Ensure the image is in RGB format and resized to 640x640
    if image.shape[2] == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    image = cv2.resize(image, (640, 640))
    # Convert the image to a tensor and normalize
    image_tensor = torch.tensor(image).float().permute(2, 0, 1).unsqueeze(0) / 255.0
    print(image_tensor.shape)
    
    result = model.detect(image_tensor)
    print(result)
    image = model.draw_detections(result[0])
    # Display the images
    cv2.imshow('Color Image', image)
    
    # check for user input to close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

# close all windows
cv2.destroyAllWindows()
cam.stop()
    