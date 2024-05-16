import subprocess
import sys

# List of libraries you want to ensure are installed
required_libraries = [
    "numpy", # numerical computing
    "python-dotenv", # environment variables
    "ultralytics", # yolo model
    "adafruit-circuitpython-servokit", # servo control
    "googlemaps", # gps
    "polyline", # polyline encoding
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
    "Adafruit-Blinka==6.15.0", # adafruit lib
    "adafruit-circuitpython-busdevice==5.1.1", # adafruit lib
    "adafruit-circuitpython-motor==3.3.4", # adafruit lib
    "adafruit-circuitpython-pca9685==3.4.0", # pca9685 driver
    "adafruit-circuitpython-register==1.9.7", # adafruit lib
    "adafruit-circuitpython-servokit==1.3.6", # adafruit lib
    "Adafruit-PlatformDetect==3.19.4",# adafruit lib
    "Adafruit-PureIO==1.1.9", # adafruit lib
    "approxeng.input", # adafruit lib ==2.6.3
    "PyYAML==6.0", # required library for approxeng
    "pathfinding", # pathfinding
    "matplotlib", # Plot lib
]

failed_libraries = []

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package])

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
