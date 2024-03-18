 # NavigateNCount 

Leveraging the YOLOv8 model for precise object detection, integrating depth maps for collision avoidance, and incorporating a GPS receiver alongside the Google Maps API, to create a comprehensive system for autonomous navigation and obstacle avoidance.

![RC Car Build](/docs/images/rc_car.jpg)

### Abstract
This project adopts a multi-sensor approach, harnessing depth data, RGB data, NMEA data, and the Google API to enable dynamic navigation across various scenarios. It employs YOLOv8, a cutting-edge object detection model, to identify and quantify objects encountered during navigation. This integrated framework offers real-time insights through computer vision techniques.

Furthermore, this approach emphasizes cost-effectiveness. By leveraging affordable sensors and open-source software, the project achieves its objectives without exorbitant expenses. This low-cost strategy ensures accessibility and scalability, making it an attractive solution for diverse applications requiring dynamic navigation and object detection capabilities.



### Result


https://github.com/DJ200148/4-car-following/assets/72373027/6540fe27-aac6-4f53-aa60-5784a06856b3


[![Object Avoidance Demo]()](https://drive.google.com/file/d/1BJGMtsHnUzpo0R-g2AMyS3Ler2OTes1d/view?t=2)


[![Depth Demo]()](https://drive.google.com/file/d/1yOQBzDLMZaiBEssIfaMJooBLiN65jjHp/view?usp=drive_link)


## Machine Learning Used

### Counter based on YOLOv8
In this project we use YOLOv8 nano model for detection and counting, below is an image showing the counter working. 

![Counter Working](/docs/images/YoloTestRoad.png)

### Depth Algorithm for Object Detection and Avoidance
Segmented data from RC POV in order to make a depth map to check for objects in the way.

![Depth detection Working](/docs/images/RCcarPOV.png)

## Setting Up and Using
### Software and Hardware Requirement 
- Python 3.8 or later.

- PyTorch 1.8 or later

- Intel RealSense SDK

- Jetson TX2 or any developer board

- Google Maps API key.

- Gps receiver(VFAN usb ug-358)

- RGBD camera(Intel D435i)

- PCA9685 board

- Traxxas RC or any similar RC  

For hardware setup, go to this YouTube [link](https://www.youtube.com/playlist?list=PLXYLzZ3XzIbi3djynrdC1ofn-54WpIFbN) to set up your RC car. We also included some of the files that were used in the video in our repo.


### Software Setup
For software setup, follow these steps:

1. Clone the repository to your desktop

2. Run the check_install_libraries.py in the root directory to install all the required libraries

    3. Set up a .env file with Google API key or adjust google_maps.py in class erase env loader and set key = to Google API key

Running our code:

1. Run the main.py in src to run our code

2. Navigate to the IP address of the jetson board, or the IP address of your board, with port 5000 where the web interface is hosted
    . ex: 192.168.0.16:5000


3. On the web interface, click on the status icon and if the status says "ready" then everything is setup properly. If not ready, then check the terminal for errors. 



### Web Interface 
![Image of Web Interface Depth Stream](/docs/images/UI_Depth_Example.PNG)

The web interface is hosted on the Jetson board using Flask and can be accessed by navigating to the IP address of the Jetson board, or the IP address of your board, with port 5000 for testing purposes.
- Start: Allows the user to input the destination coordinates and start the car.
- Status: Returns the status of the car. ("ready", "running", "stopped", "paused")
- Pause: Pauses the car.
- Resume: Resumes the car.
- Reset: Resets the car to the ready state.
- Shutdown: Shut down the entire system.
- Stream Play: Starts the stream of the camera.
- Stream Stop: Stops the stream of the camera.
- Depth Play: Starts the depth stream and stops the RGB stream.
- Depth Stop: Stops the depth and start the RGB stream.

## Design and Implementation

### Pipeline
![Image of Pipeline](/docs/images/pipeline.png)

First, the camera provides RGB and depth data; the former is processed asynchronously in the image thread. Depth data undergoes analysis, influencing whether the RC must avoid obstacles. Prioritizing safety, collision avoidance activates the protocol to safely navigate around obstacles, realigning with the intended path, and following a polyline route. When not avoiding obstacles, the RC assesses its local position globally using GPS data, adjusting its direction based on orientation and polyline cues. Upon nearing a polyline endpoint, it aligns to the next segment. This cycle repeats throughout the operation.

### Object Avoidance and Camera
The navigation protocol is very simple, where when an obstacle is detected the car will navigate its way around it using synchronous time delays. We plan on adding more advanced methods such as road segmentation, lane detection, and advanced path planning in the future.

### Steering and Throttle Controls
After you have followed the youtube, the car should be able to move forward and backward and turning left, right, and repeat.

https://github.com/DJ200148/4-car-following/assets/72373027/09a12043-bf78-4df7-832b-312d38e76a95



### GPS and Path Following

After allowing a minute for satellite tracking, the GPS receiver begins to furnish real-time coordinates. These coordinates, along with user-provided destination coordinates, are
relayed to Google's API, which generates a navigational path for the car. Subsequently, the GPS receiver continuously updates the current coordinates, while the car dynamically
navigates by following the path provided by the API. If the car reaches within 5m of the coordinate the coordinate is popped from the queue. To ensure alignment with the intended
direction of travel, the car adjusts its orientation using vector and angle mathematics.



# Acknowledgement
Kartik Patwari

Providing help with debugging and fixing broken boards. Offering assistance with any coding questions.

Professor Chen-Nee Chuah

Providing the class an opportunity to learn more about machine learning.


# Reference links

[Yolo Repository](https://github.com/ultralytics/ultralytics)

[Google Maps Services Python GitHub](https://github.com/googlemaps/google-maps-services-python.git)

[Steering and Throttle calibration](https://github.com/jetsonhacks/jetsonRACECAR)

[PCA9685 Driver](https://github.com/jetsonhacks/JHPWMDriver)

[1] Gakstatter, Eric. “What Exactly Is GPS NMEA Data? - GPS World.” GPS World - The Business and Technology of Global Navigation and Positioning, 4 Feb. 2015, www.gpsworld.com/what-exactly-is-gps-nmea-data/. 

[2] rishabsingh3003. “Rishabsingh3003/Vision-Obstacle-Avoidance:, github.com/rishabsingh3003/Vision-Obstacle-Avoidance

[YOLOv8](https://github.com/ultralytics/ultralytics)

[PCA9685 Driver](https://github.com/jetsonhacks/JHPWMDriver)

[IntelRealSense](github.com/IntelRealSense/librealsense)
