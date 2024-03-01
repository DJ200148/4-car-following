from classes.depth_camera import DepthCamera
from classes.algo_detection_helper import AlgoDetectionHelper
import cv2
import time


cam = DepthCamera()
algo = AlgoDetectionHelper()
print("Camera Initialized.")

while True:

    color_image, depth_image, depth_colormap = cam.get_image_data()
    cv2.imshow('Depth Colormap', depth_colormap)
    # cv2.imshow('Depth Image', depth_image)
    
    direction = algo.get_turn_direction_from_depth_data(depth_image, threshold=700)

    print(direction)


    # If the 'q' key is pressed, break out of the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()

