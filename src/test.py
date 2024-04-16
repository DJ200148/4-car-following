from classes.depth_camera import DepthCamera
import cv2
from classes.yolo_model import YoloModel


cam = DepthCamera()
model = YoloModel('../weights/yolov8n.pt')

print("Init done")

while True:
    image, depth, depth_colormap = cam.get_image_data()
    result = model.detect(image)
    # print(result)
    image = model.draw_detections(result[0])
    # Display the images
    cv2.imshow('Color Image', image)
    
    # check for user input to close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

# close all windows
cv2.destroyAllWindows()
cam.stop()
    