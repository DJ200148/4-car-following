from classes.yolop_model import YolopModel
from classes.control_system import ConstrolSystem
from classes.gps import GPS
from classes.depth_camera import DepthCamera
from classes.depth_detection import DepthDetection
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
        pass

    def run(self):
        while True:
            self.decide_action()
            pass
        pass

    def pause(self):
        pass

    def decide_action(self):
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

