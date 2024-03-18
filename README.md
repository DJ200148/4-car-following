![front image or gif](To do)

# NavigateNCount 

Leveraging the YOLOv8 model for precise object detection, integrating depth maps for collision avoidance, and incorporating a GPS receiver alongside the Google Maps API,  to create a comprehensive system for autonomous navigation and obstacle avoidance.

# Introduction 
##### Abstract
this project employs a multi-sensor approach, utilizing depth data, RGB data, NMEA data, and the Google API to facilitate dynamic navigation across diverse scenarios. Simultaneously, the system incorporates YOLOv8, a state-of-the-art object detection model, to not only identify but also quantify objects encountered along its traversed path. This integrated framework provides real-time insights by leveraging advanced computer vision techniques for object detection and counting.


##### Result
[![Demo]()](https://drive.google.com/file/d/1BJGMtsHnUzpo0R-g2AMyS3Ler2OTes1d/view?t=2)


https://github.com/DJ200148/4-car-following/assets/72373027/440c3f56-3f83-4705-a6d8-1721f2e0646b


https://github.com/DJ200148/4-car-following/blob/main/rc_avoidance_demo2.MOV

# Using ML

##### YOLOv8 Model

##### Depth Algorithm

# Setting up
#### Software and Hardware Requirement 
Python 3.8 or later.

Jetson TX2 or any developer board

Google Maps API key.

Gps receiver

RGBD camera

PCA9685 board

Traxxas RC or any similar RC 

For hardware setup, go to this youtube [link](https://www.youtube.com/playlist?list=PLXYLzZ3XzIbi3djynrdC1ofn-54WpIFbN) to setup your RC car. We also included some of the files that were used in the video in our repo.

For software setup, follow these steps:

    1. Clone the repository to your desktop

    2. Run the check_install_libraries.py

Running our code:

    1. Run the main.py in src to run our code

    2. Navigate to the ip address of the jetson board, or the ip address of your board, with port 5000 where the web interface is hosted
       ex: 192.168.0.16:5000 
    3. On the web interface, click on status icon and if the status says "ready" then everything is setup properly. If not ready, then check the terminal for errors. 

# Design and Implementation

##### Pipeline

##### 
# Testing

##### Object Avoidance and Camera

##### Steering and Throttle Controls

##### GPS and Path Following

# Web Interface 



# Acknowledgement
Kartik Patwari

Professor Chen-Nee Chuah

Sharama

Chat GPT


# Reference links
[Yolo Repository](https://github.com/ultralytics/ultralytics)

[Google Maps Services Python GitHub](https://github.com/googlemaps/google-maps-services-python.git)

[Steering and throtlle calibration](https://github.com/jetsonhacks/jetsonRACECAR)
