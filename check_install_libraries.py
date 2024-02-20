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
    "onnxruntime", # onnx model runtime
    "torch", # pytorch
    "torchvision", # pytorch vision
    "prefetch_generator", # prefetch data
    "yacs", # yet another configuration system
    "scikit-learn", # machine learning
    "Flask", # web framework
]

failed_libraries = []

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for lib in required_libraries:
    try:
        try:
            __import__(lib)
            print(f"{lib} is already installed.")
        except ImportError:
            print(f"{lib} not found, installing...")
            install(lib)
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Failed to install {lib}.")
        failed_libraries.append(lib)

if len(failed_libraries) > 0:
    print(f"Failed to install the following libraries: {failed_libraries}")
else:
    print("All required libraries are installed.")
