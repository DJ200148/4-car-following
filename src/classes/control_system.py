from adafruit_servokit import ServoKit
import board
import busio

# Servo Throttle Speeds
MAX_THROTTLE = 60
MIN_THROTTLE = 0
BASE_THROTTLE = 30

# Servo Turn Angles
MAX_TURN_ANGLE = 90
MIN_TURN_ANGLE = -90
CENTER_TURN_ANGLE = 90

# Servo Channels
SERVO_CHANNEL = 0
THROTTLE_CHANNEL = 1

class ConstrolSystem:
    def __init__(self):
        print("Initializing Control System")
        i2c_bus = busio.I2C(board.SCL, board.SDA)
        print("Initializing Servo Kit")
        self.kit = ServoKit(channels=16, address=0x40, i2c=i2c_bus)
        print("Initializing Controller")
        self.turn_center()

    def forward(self, speed=BASE_THROTTLE):
        speed = max(MIN_THROTTLE, min(MAX_THROTTLE, speed))
        self.kit.continuous_servo[THROTTLE_CHANNEL].throttle = speed / 100

    def reverse(self, speed=BASE_THROTTLE):
        speed = max(MIN_THROTTLE, min(MAX_THROTTLE, speed))
        self.kit.continuous_servo[THROTTLE_CHANNEL].throttle = -speed / 100
        
    def brake(self):
        self.kit.continuous_servo[THROTTLE_CHANNEL].throttle = 0
    
    def turn_center(self):
        self.kit.servo[SERVO_CHANNEL].angle = CENTER_TURN_ANGLE
    
    def turn(self, angle=CENTER_TURN_ANGLE):
        angle = max(MIN_TURN_ANGLE, min(MAX_TURN_ANGLE, angle))
        self.kit.servo[SERVO_CHANNEL].angle = CENTER_TURN_ANGLE + angle
        