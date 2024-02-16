from classes.detection_model import DetectionModel
from classes.control_system import ConstrolSystem
from Gps.Gps import Gps


# Here we will combine all the pipelines and run them in a sequence

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
gps = Gps()
camera = CameraModel()
rc_control_system = ConstrolSystem()

while True:
    # get image
    pass