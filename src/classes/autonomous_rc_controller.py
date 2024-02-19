from threading import Thread, Event
from time import sleep
# Classes
from classes.yolop_model import YolopModel
from classes.control_system import ConstrolSystem
from classes.gps import GPS
from classes.depth_camera import DepthCamera
from src.classes.also_detection_helper import DepthDetection
from classes.google_maps import GoogleMaps

# Use Cases:
# 1. The RC should turn left
# 2. The RC should turn right
# 3. The RC should go forward
# 4. The RC should be able to detect if it needs to turn around 


class AutonomousRCController:
    def __init__(self):
        self.rc = ConstrolSystem()
        self.yolop_model = YolopModel()
        self.gps = GPS()
        self.depth_camera = DepthCamera()
        self.depth_detection = DepthDetection()
        self.google_maps = GoogleMaps()

        # Init threads
        self.pause_event = Event()  # This event controls the pause state.
        self.stop_event = Event()  # This event controls the stop state to safely exit the loop.
        self.thread = Thread(target=self.run)  # Thread running the run method
        # Set the event at the start so the loop runs
        self.pause_event.set()

        # Init the start and end cords
        self.start_cords = self.gps.get_coordinates()
        self.end_cords
        self.current_cords = self.start_cords
        self.path
        self.directions

    # Operations
    def start(self, end_cords):
        self.end_cords = end_cords
        self.directions = self.google_maps.get_directions(self.start_cords, self.end_cords)
        self.path = self.google_maps.directions_to_path(self.directions)
        self.thread.start()

    def pause(self):
        self.pause_event.clear()  # Clearing the event pauses the loop

    def resume(self):
        self.pause_event.set()  # Setting the event resumes the loop

    def shutdown(self):
        self.stop_event.set()  # Indicate that the run loop should stop
        self.resume()  # If it's paused, we need to resume it to allow exit
        self.thread.join()  # Wait for the thread to finish
        
        # Clean up
        self.gps.stop()
        self.depth_camera.stop()
    
    # The main loop
    def run(self):
        while not self.stop_event.is_set():
            self.pause_event.wait()  # Wait will block if the event is cleared, simulating a pause
            self.decide_action()
            sleep(0.1)  # Adjust the sleep time as needed

    def decide_action(self):
        # Gather data for the decision
        color_image, depth_image, depth_colormap = self.depth_camera.get_image_data()
        objects = self.yolop_model.detect(color_image)
        if self.should_turn_left():
            self.rc.turn_left()
        elif self.should_turn_right():
            self.rc.turn_right()
        elif self.should_go_forward():
            self.rc.turn_center()
            self.rc.forward()
        else:
            self.rc.brake()

    def should_turn_left(self):
        pass

    def should_turn_right(self):
        pass

    def should_go_forward(self):
        pass

    # def should_reverse(self):
    #     pass

    # def should_slow_down(self):
    #     pass

    # def should_speed_up(self):
    #     pass

