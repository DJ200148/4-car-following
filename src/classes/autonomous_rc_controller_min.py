from threading import Thread, Event, Lock
from time import sleep
import numpy as np
import traceback
import cv2
from datetime import datetime
import torch

# Classes
from classes.depth_camera import DepthCamera
from classes.status_enum import Status
from classes.yolo_model import YoloModel

class AutonomousRCController():
    def __init__(self, test_mode=False, low_threshold=400, high_threshold=700, offset=7, save_dir='./output'):
        self.test_mode = test_mode
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.offset = offset
        self.save_dir = save_dir
        self.status = Status.READY
        
        self.yolo_model = YoloModel(model_name='./weights/yolov8n.pt', device='cuda')
        self.depth_camera = DepthCamera()

        # Init threads
        self.pause_event = Event()  # This event controls the pause state.
        self.stop_event = Event()  # This event controls the stop state to safely exit the loop.
        # self.yolo_capture_event = Event()
        # self.yolo_capture_thread = None
        self.thread = Thread(target=self.run)  # Thread running the run method
        # Set the event at the start so the loop runs
        self.pause_event.set()

        # Init the start and end cords
        self.start_cords = None
        self.end_cords = None
        self.directions = None
        self.path = None
        self.prev_path_target = None
        self.curr_path_target = None
        
        self.detect_buf = None
        self.detect_lock = Lock()

    
    def get_status(self):
        return self.status

    def reset(self):
        self.stop() # Stop the system
        # reset rc
        self.depth_camera = DepthCamera()

        # Init threads
        self.pause_event = Event()  # This event controls the pause state.
        self.stop_event = Event()  # This event controls the stop state to safely exit the loop.
        self.thread = Thread(target=self.run)  # Thread running the run method
        # Set the event at the start so the loop runs
        self.pause_event.set()

        self.status = Status.READY
        

    # Operations
    def start(self, end_cords=None):
        if self.status != Status.READY:
            raise RuntimeError("The controller is not ready to start")

        # start normal pipeline
        self.thread.start()
        self.status = Status.RUNNING

    def pause(self):
        if self.status == Status.RUNNING:
            # self.rc.disable_controls()
            self.pause_event.clear()  # Clearing the event pauses the loop
            self.status = Status.PAUSED

    def resume(self):
        if self.status == Status.PAUSED:
            # self.rc.enable_controls()
            self.pause_event.set()  # Setting the event resumes the loop
            self.status = Status.RUNNING

    def stop(self):
        self.status = Status.PAUSED
        self.stop_event.set()  # Indicate that the run loop should stop
        self.resume()  # If it's paused, we need to resume it to allow exit
        if self.thread.is_alive():  # Check if the thread has been started and is still running
            self.thread.join()  # Wait for the thread to finish
        self.status = Status.STOPPED
        
        # Clean up
        self.depth_camera.stop()


    # The main loop
    def run(self):
        try:
            while not self.stop_event.is_set():
                try:
                    self.pause_event.wait()  # Wait will block if the event is cleared, simulating a pause
                    if self.stop_event.is_set(): break
                    
                    # Get image data
                    image, _, _ = self.depth_camera.get_image_data()
                    print(torch.cuda.is_available())
                    # Convert image to the models specs (RGB format and resized to 640x640)
                    if image.shape[2] == 1:
                        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                    elif image.shape[2] == 4:
                        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
                    else:
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    
                    image = cv2.resize(image, (640, 640))
                    
                    # Convert the image to a tensor and normalize
                    image_tensor = torch.tensor(image).float().permute(2, 0, 1).unsqueeze(0) / 255.0
                    print("performing detection")
                    # Perform detection
                    results = self.yolo_model.detect(image_tensor)
                    print("draw boxes")
                    # Calulate bounding boxes and count (Look into any pre built methods that work with yolo to count and detect)
                    image_with_detections = self.yolo_model.draw_detections(image, results)
                    
                    print("use lock to update image")
                    # Save image to buffer for UI to gather (Concurrent safe buffer?)
                    with self.detect_lock:
                        self.detect_buf = image_with_detections
                    
                    # Repeat till paused
                except Exception as ex:
                    print(ex)
                    pass
                    
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()  # This prints the traceback details
        finally:
            # Ensure the video recording thread is stopped properly
            # self.yolo_capture_event.set()
            # if self.video_capture_thread is not None:
            #     self.video_capture_thread.join()
            pass
    
    def get_latest_detect_image(self):
        with self.detect_lock:
            image = self.detect_buf
            if image is None:
                return None
        # if image == None:
        #     return 
        # Convert the color image to a JPEG frame
        ret, jpeg_frame = cv2.imencode('.jpg', image)
        if not ret:
            return None
        
        # Return the JPEG frame
        return jpeg_frame.tobytes() 

