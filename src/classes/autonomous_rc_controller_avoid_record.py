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
from classes.helpers import get_turn_direction_from_depth_data
from classes.google_maps import GoogleMaps
from classes.status_enum import Status
# from classes.autonomous_rc_controller_interface import AutonomousRCControllerInterface

class AutonomousRCController():
    def __init__(self, test_mode=False, low_threshold=400, high_threshold=700, offset=7, save_dir='./output'):
        self.test_mode = test_mode
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.offset = offset
        self.save_dir = save_dir
        self.status = Status.READY
        
        self.rc = ConstrolSystem(self.offset)
        # self.yolop_model = YolopModel()
        # self.gps = GPS()
        self.depth_camera = DepthCamera()
        # self.google_maps = GoogleMaps()

        # Init threads
        self.pause_event = Event()  # This event controls the pause state.
        self.stop_event = Event()  # This event controls the stop state to safely exit the loop.
        self.yolo_capture_event = Event()
        self.yolo_capture_thread = None
        self.thread = Thread(target=self.run)  # Thread running the run method
        # Set the event at the start so the loop runs
        self.pause_event.set()

        # Init the start and end cords
        
        # self.prev_cords
        # self.start_cords
        # self.end_cords
        # self.curr_path_target
        # self.path
        # self.directions
        # self.current_cords = self.start_cords
        # self.previous_cords = self.start_cords
        # self.current_orientation
        # self.desired_orientation
        # wait for all components to be ready

    
    
    # @property
    # def curr_cords(self):
    #     return self.gps.get_coordinates()
    
    def get_status(self):
        return self.status

    def reset(self):
        self.stop() # Stop the system
        # reset rc
        self.depth_camera = DepthCamera()
        self.rc = ConstrolSystem(self.offset)
        # self.gps = GPS())
        # self.google_maps = GoogleMaps()

        # Init threads
        self.pause_event = Event()  # This event controls the pause state.
        self.stop_event = Event()  # This event controls the stop state to safely exit the loop.
        self.thread = Thread(target=self.run)  # Thread running the run method
        # Set the event at the start so the loop runs
        self.pause_event.set()

        # Init the start and end cords
        # self.start_cords = self.gps.get_coordinates()
        # self.current_cords = self.start_cords
        # self.previous_cords = self.start_cords
        # self.current_orientation = self.current_orientation
        # self.desired_orientation = self.desired_orientation
        self.status = Status.READY
        

    # Operations
    def start(self, end_cords):
        if self.status != Status.READY:
            raise RuntimeError("The controller is not ready to start")
        # Set cords
        # self.prev_cords = self.curr_cords
        # self.start_cords = self.curr_cords
        # self.end_cords = end_cords

        # Get the directions and path
        # self.directions = self.google_maps.get_directions(self.start_cords, self.end_cords)
        # self.path = self.google_maps.directions_to_path(self.directions)
        # self.curr_path_target = self.path.pop()

        # calibrate the position of the RC
        # self.calibrate_position()

        # start normal pipeline
        self.thread.start()
        self.status = Status.RUNNING

    def pause(self):
        if self.status == Status.RUNNING:
            self.rc.disable_controls()
            self.pause_event.clear()  # Clearing the event pauses the loop
            self.status = Status.PAUSED

    def resume(self):
        if self.status == Status.PAUSED:
            self.rc.enable_controls()
            self.pause_event.set()  # Setting the event resumes the loop
            self.status = Status.RUNNING

    def stop(self):
        self.status = Status.PAUSED
        self.stop_event.set()  # Indicate that the run loop should stop
        self.resume()  # If it's paused, we need to resume it to allow exit
        self.rc.disable_controls()
        if self.thread.is_alive():  # Check if the thread has been started and is still running
            self.thread.join()  # Wait for the thread to finish
        self.status = Status.STOPPED
        
        # Clean up
        # self.gps.stop()
        self.depth_camera.stop()

    def start_video_capture(self):
        self.yolo_capture_event.clear()
    
        # Get the current date
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d-[%H-%M]')
        self.video_writer = cv2.VideoWriter(f'{self.save_dir}/{formatted_datetime}-capture.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))
        
        while not self.yolo_capture_event.is_set():
            color_image, _, _ = self.depth_camera.get_image_data()
            if color_image is not None:
                self.video_writer.write(color_image)
        
        self.video_writer.release()

    # The main loop
    def run(self):
        try:
             # Start the video capture thread
            self.yolo_capture_event.clear()
            self.video_capture_thread = Thread(target=self.start_video_capture)
            self.video_capture_thread.start()
            
            while not self.stop_event.is_set():
                self.pause_event.wait()  # Wait will block if the event is cleared, simulating a pause
                if self.stop_event.is_set(): break # 
                _, depth_image, _ = self.depth_camera.get_image_data()
                if depth_image is not None:
                    # decide action
                    direction = get_turn_direction_from_depth_data(depth_image, low_threshold=self.low_threshold, high_threshold=self.high_threshold)
                    if self.test_mode: print(direction)
                    
                    # default speed and angle for calibration
                    speed = 65
                    angle = 35
                    turn_delay = .75
                    forward_delay = .75
                    full_turn_delay = 1.9
                    if direction == 'forward':
                        self.do_forward_action(speed)
                    elif direction == 'right':
                        self.make_right_turn_around_obstacle(speed, angle, turn_delay, forward_delay, full_turn_delay)
                    elif direction == 'left':
                        self.make_left_turn_around_obstacle(speed, angle, turn_delay, forward_delay, full_turn_delay)
                    else:
                        self.rc.brake()

                    # self.decide_action(depth_image)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()  # This prints the traceback details
            self.rc.disable_controls()
        finally:
            # Ensure the video recording thread is stopped properly
            self.yolo_capture_event.set()
            if self.video_capture_thread is not None:
                self.video_capture_thread.join()

    def do_forward_action(self, speed):
        # go straight
        self.rc.turn()
        self.rc.forward(speed)

        # check the current position and orientation of the RC then make any nessary adjustments for the global direction


    def make_right_turn_around_obstacle(self, speed, angle, turn_delay, forward_delay, full_turn_delay):
        # turn right
        self.rc.forward(speed)
        self.rc.turn(angle)
        sleep(turn_delay)

        # go straight
        self.rc.turn()
        sleep(forward_delay)

        # turn left
        self.rc.turn(-angle)
        sleep(full_turn_delay)

        # go straight
        self.rc.turn()
        sleep(forward_delay/2)

        # turn right
        self.rc.turn(angle)
        sleep(turn_delay)

        # go straight
        self.rc.turn()

    def make_left_turn_around_obstacle(self, speed, angle, turn_delay, forward_delay, full_turn_delay):
        # turn left
        self.rc.forward(speed)
        self.rc.turn(-angle)
        sleep(turn_delay)

        # go straight
        self.rc.turn()
        sleep(forward_delay)

        # turn right
        self.rc.turn(angle)
        sleep(full_turn_delay)

        # go straight
        self.rc.turn()
        sleep(forward_delay/2)

        # turn left
        self.rc.turn(-angle)
        sleep(turn_delay)

        # go straight
        self.rc.turn()
    
    # def decide_action(self, depth_image):
    #     # Gather data for the decision
    #     direction = get_turn_direction_from_depth_data(depth_image, low_threshold=self.low_threshold, high_threshold=self.high_threshold)
    #     if self.test_mode: print(direction)
        
    #     speed = 70
    #     if direction == 'forward':
    #         self.rc.turn()
    #         self.rc.forward(speed)
    #     elif direction == 'right':
    #         self.rc.turn(35)
    #         self.rc.forward(speed)
    #     elif direction == 'left':
    #         self.rc.turn(-35)
    #         self.rc.forward(speed)
    #     else:
    #         self.rc.brake()

    #     pass

    def get_orientation(coor, compared_coor):
        """based off of 2 given coordinates calculates degree to 2nd coordinate N=0"""
        new_origin_coor = (compared_coor[0] - coor[0],compared_coor[1]-coor[1])
        orientation = np.mod(np.degrees(np.arctan2(new_origin_coor[1],new_origin_coor[0])),360)
        return orientation

# def calibrate_position(self):
    #     # JAMES: You can implement this method to a get the RC car to the correct position
        #
        # self.current_orientation = get_orientation(self.previous_coords, self.current_cords)
        # self.desired_orientation = get_orientation(self.current_coords, self.path[0])
        # angle = (self.desired_orientation - self.current_orientation) % 360
        # angle = (angle-180)%360 +180 
        #if(angle < 0)
        # should turn left
        #elif(angle > 0)
        # should turn right
        #else
        #should go straight
    #     pass
