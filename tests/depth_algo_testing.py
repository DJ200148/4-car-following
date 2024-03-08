from classes.depth_camera import DepthCamera
from classes.helpers import get_turn_direction_from_depth_data, display_depth_colormap
import cv2
import time


cam = DepthCamera()
print("Camera Initialized.")

while True:

    color_image, depth_image, depth_colormap = cam.get_image_data()
    
    direction = get_turn_direction_from_depth_data(depth_image, low_threshold=400, high_threshold=700)
    print(direction)
    
    display_depth_colormap(depth_colormap)

    # If the 'q' key is pressed, break out of the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()

