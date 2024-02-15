# Here we will combine all the pipelines and run them in a sequence
from classes.detectionModel import DetectionModel
from Gps.Gps import Gps

# Real time is 24 fps

# Pipeline Steps
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


# Initialize
yolo_model = DetectionModel()
gps_model = Gps()
camera_model = CameraModel()
rc_model = RCModel()
    
while True:
    # get image
    pass