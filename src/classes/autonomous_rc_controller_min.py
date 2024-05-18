from threading import Thread, Event
from time import sleep
import numpy as np
import traceback
import cv2
from datetime import datetime

# Classes
# from classes.yolop_model import YolopModel
from classes.control_system import ConstrolSystem
from classes.gps import GPS
from classes.depth_camera import DepthCamera
from classes.helpers import get_turn_direction_from_depth_data, calculate_relative_direction, distance_between_points_cartesian
from classes.google_maps import GoogleMaps
from classes.status_enum import Status
from classes.yolop_model import YolopModel
# from classes.autonomous_rc_controller_interface import AutonomousRCControllerInterface

class AutonomousRCController():
    def __init__(self, test_mode=False, low_threshold=400, high_threshold=700, offset=7, save_dir='./output'):
        self.test_mode = test_mode
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.offset = offset
        self.save_dir = save_dir
        self.status = Status.READY
        
        self.yolop_model = YolopModel()
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
    def start(self, end_cords):
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

    # def start_video_capture(self):
    #     self.yolo_capture_event.clear()
    
    #     # Get the current date
    #     current_datetime = datetime.now()
    #     formatted_datetime = current_datetime.strftime('%Y-%m-%d-[%H-%M]')
    #     self.video_writer = cv2.VideoWriter(f'{self.save_dir}/{formatted_datetime}-capture.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))
        
    #     while not self.yolo_capture_event.is_set():
    #         color_image, _, _ = self.depth_camera.get_image_data()
    #         if color_image is not None:
    #             self.video_writer.write(color_image)
        
    #     self.video_writer.release()

    # The main loop
    def run(self):
        try:
             # Start the video capture thread
            # self.yolo_capture_event.clear()
            # self.video_capture_thread = Thread(target=self.start_video_capture)
            # self.video_capture_thread.start()
            
            while not self.stop_event.is_set():
                self.pause_event.wait()  # Wait will block if the event is cleared, simulating a pause
                if self.stop_event.is_set(): break
                _, depth_image, _ = self.depth_camera.get_image_data()
                
                
                
                
                    
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()  # This prints the traceback details
        finally:
            # Ensure the video recording thread is stopped properly
            # self.yolo_capture_event.set()
            # if self.video_capture_thread is not None:
            #     self.video_capture_thread.join()


    
