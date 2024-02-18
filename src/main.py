# Here we will combine all the pipelines and run them in a sequence

# Imports
from classes.yolo_model import YoloModel
from classes.control_system import ConstrolSystem
from classes.gps import GPS
from classes.depth_camera import DepthCamera
from classes.depth_detection import DepthDetection
from classes.google_maps_system import GoogleMapsSystem


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

# Initialize
yolo_model = DetectionModel()
gps = Gps()
camera = CameraModel()
rc_control_system = ConstrolSystem()


while True:

    # If the system is stopped, then wait
    while STOP:
        pass


    # get image
    pass