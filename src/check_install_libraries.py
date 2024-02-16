import subprocess
import sys

# List of libraries you want to ensure are installed
required_libraries = [
    "numpy", # numerical computing
    "python-dotenv", # environment variables
    "ultralytics", # yolo model
    "adafruit-circuitpython-servokit", # servo control
    "googlemaps", # gps
    "opencv-contrib-python", # computer vision
    "pyrealsense2", # depth camera
    "pyserial", # serial communication
    "geopy", # geolocation tools
]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for lib in required_libraries:
    try:
        __import__(lib)
        print(f"{lib} is already installed.")
    except ImportError:
        print(f"{lib} not found, installing...")
        install(lib)

print("All required libraries are installed.")
