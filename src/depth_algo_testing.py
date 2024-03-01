from classes.depth_camera import DepthCamera
import cv2


cam = DepthCamera()
print("Camera Initialized.")
color_image, depth_image, depth_colormap = cam.get_image_data()
print("Image Data Gathered.")
# Display the images
cv2.imshow('Color Image', color_image)
cv2.imshow('Depth Colormap', depth_colormap)  # Display the depth colormap for visualization

while True:
    # wait for the user to press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.stop()  # Ensure to stop the camera after exiting the loop
cv2.destroyAllWindows()  # Close all OpenCV windows
