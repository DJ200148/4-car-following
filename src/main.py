# Here we will combine all the pipelines and run them in a sequence

# Imports
# from classes.autonomous_rc_controller import AutonomousRCController
from classes.depth_camera import DepthCamera
import cv2


#### NOTES ####
# Real time is 24 fps

## Pipeline Steps
# Init all nessary classes and helpers
# Check the GPS locations of where you start and end
# Find the shortest path between the two points that is drivable
# if no path notfiy the user

# Loop
# Get GPS location
# ensure that the rc is on the shortest path, if not then correct it
# Gather input data from the camera (image + depth)
# Detect objects in the input data
# determine if the rc needs to avoid an object via the detection and distances
# make any nessary adjustments to the rc,
    # like slowing down, stopping, turning or reversing
### END NOTES ###

# Constants
STOP = False
END_CORDS = (0, 0)

if __name__ == "__main__":
    # controller = AutonomousRCController()
    # controller.start(END_CORDS)
    # while True:
    #     if STOP:
    #         controller.stop()
    #         break

    #     pass
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

        