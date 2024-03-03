from threading import Thread, Event
from time import sleep
import numpy as np
import traceback

# Classes
# from classes.yolop_model import YolopModel
from classes.control_system import ConstrolSystem
from classes.gps import GPS
from classes.depth_camera import DepthCamera
from classes.helpers import get_turn_direction_from_depth_data, display_depth_colormap
from classes.google_maps import GoogleMaps


class AutonomousRCController:
    def __init__(self, test_mode=False, low_threshold=400, high_threshold=700, offset=7):
        self.test_mode = test_mode
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.offset = offset
        
        self.rc = ConstrolSystem(self.offset)
        # self.yolop_model = YolopModel()
        # self.gps = GPS(port='/dev/ttyUSB0')
        self.depth_camera = DepthCamera()
        # self.google_maps = GoogleMaps()

        # Init threads
        self.pause_event = Event()  # This event controls the pause state.
        self.stop_event = Event()  # This event controls the stop state to safely exit the loop.
        self.thread = Thread(target=self.run)  # Thread running the run method
        # Set the event at the start so the loop runs
        self.pause_event.set()

        # Init the start and end cords
        # self.start_cords = self.gps.get_coordinates()
        # self.end_cords
        # self.current_cords = self.start_cords
        # self.previous_cords = self.start_cords
        # self.path
        # self.directions
        # self.current_orientation
        # self.desired_orientation
        # wait for all components to be ready
    
    def reset(self):
        self.stop() # Stop the system
        # reset rc
        self.rc = ConstrolSystem(self.offset)
        self.depth_camera = DepthCamera()

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
        

    # Operations
    def start(self, end_cords):
        # self.end_cords = end_cords
        # self.directions = self.google_maps.get_directions(self.start_cords, self.end_cords)
        # self.path = self.google_maps.directions_to_path(self.directions)

        # calibrate the position of the RC
        # self.calibrate_position()

        # start normal pipeline
        self.thread.start()

    def pause(self):
        self.rc.disable_controls()
        self.pause_event.clear()  # Clearing the event pauses the loop

    def resume(self):
        self.rc.enable_controls()
        self.pause_event.set()  # Setting the event resumes the loop

    def stop(self):
        self.rc.disable_controls()
        self.stop_event.set()  # Indicate that the run loop should stop
        self.resume()  # If it's paused, we need to resume it to allow exit
        self.thread.join()  # Wait for the thread to finish
        
        # Clean up
        # self.gps.stop()
        self.depth_camera.stop()

    # The main loop
    def run(self):
        try:
            while not self.stop_event.is_set():
                self.pause_event.wait()  # Wait will block if the event is cleared, simulating a pause
                color_image, depth_image, depth_colormap = self.depth_camera.get_image_data()
                if self.test_mode: display_depth_colormap(depth_colormap)
                self.decide_action(depth_image)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()  # This prints the traceback details
            self.rc.disable_controls()

    def decide_action(self, depth_image):
        # Gather data for the decision
        direction = get_turn_direction_from_depth_data(depth_image, low_threshold=self.low_threshold, high_threshold=self.high_threshold)
        if self.test_mode: print(direction)
        
        if direction == 'forward':
            self.rc.turn()
            self.rc.forward(60)
        elif direction == 'right':
            self.rc.turn(35)
            self.rc.forward(60)
        elif direction == 'left':
            self.rc.turn(-35)
            self.rc.forward(60)
        else:
            self.rc.brake()

        pass

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