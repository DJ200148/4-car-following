from adafruit_servokit import ServoKit
import board
import busio
import subprocess

# Servo Throttle Speeds
MAX_THROTTLE = 60
MIN_THROTTLE = 0
BASE_THROTTLE = 30

# Servo Turn Angles
MAX_TURN_ANGLE = 90
CENTER_TURN_ANGLE = 0
MIN_TURN_ANGLE = -90
BASE_TURN_ANGLE = 90



# Servo Channels
SERVO_CHANNEL = 0
THROTTLE_CHANNEL = 1

class ConstrolSystem:
    def __init__(self, offset=7, shutdown_pin='466'):
        # Postive offset goes right
        self.offset = offset
        self.shutdown_pin = shutdown_pin
        print("Initializing Control System")
        self.enable_controls()
        
        print("Shutdown pin enabled")
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
        self.kit.servo[SERVO_CHANNEL].angle = BASE_TURN_ANGLE + self.offset
    
    def turn(self, angle=CENTER_TURN_ANGLE):
        angle = max(MIN_TURN_ANGLE, min(MAX_TURN_ANGLE, angle))
        self.kit.servo[SERVO_CHANNEL].angle = BASE_TURN_ANGLE + angle + self.offset
    
    def disable_controls(self):
        self.set_gpio_value(1)

    def enable_controls(self):
        self.set_export_gpio()
        self.set_direction_gpio()
        self.set_gpio_value(0)
    
    def set_export_gpio(self):
        # Export the GPIO pin
        subprocess.run(['echo', str(self.shutdown_pin), '>', '/sys/class/gpio/export'])
    
    def set_direction_gpio(self, direction='out'):
        # Set the direction of the GPIO pin to "out"
        subprocess.run(['echo', str(direction), '>', f'/sys/class/gpio/gpio{self.shutdown_pin}/direction'])
    
    def set_gpio_value(self, value):
        # Set the value of the GPIO pin
        subprocess.run(['echo', str(value), '>', f'/sys/class/gpio/gpio{self.shutdown_pin}/value'])