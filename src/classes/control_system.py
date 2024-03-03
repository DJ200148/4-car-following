from adafruit_servokit import ServoKit
import board, busio, subprocess, os, time

# Servo Throttle Speeds
MAX_THROTTLE = 90
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
        print("Initializing Control System")
        self.offset = offset
        self.shutdown_pin = shutdown_pin
        print("Initializing Shutdown Pin")
        self.enable_controls()
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
        self.set_export_gpio(self.shutdown_pin)
        self.set_direction_gpio()
        self.set_gpio_value(0)
    
    def run_command(self, command):
        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Command executed successfully: {command}")
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {command}\nError: {e}")

    def wait_for_gpio_ready(self, gpio_path, timeout=5):
        start_time = time.time()
        while not os.path.exists(gpio_path):
            time.sleep(0.1)  # Wait for 100ms
            if time.time() - start_time > timeout:
                raise TimeoutError(f"GPIO path {gpio_path} did not become available within {timeout} seconds.")

    def set_export_gpio(self, gpio_pin):
        gpio_path = f'/sys/class/gpio/gpio{gpio_pin}'

        if not os.path.exists(gpio_path):
            self.run_command(f'echo {gpio_pin} > /sys/class/gpio/export')
            self.wait_for_gpio_ready(gpio_path)
        else:
            print(f"GPIO {gpio_pin} is already exported.")

    def set_direction_gpio(self, direction='out'):
        direction_path = f'/sys/class/gpio/gpio{self.shutdown_pin}/direction'
        self.wait_for_gpio_ready(direction_path)
        self.run_command(f'echo {direction} > {direction_path}')

    def set_gpio_value(self, value):
        value_path = f'/sys/class/gpio/gpio{self.shutdown_pin}/value'
        self.wait_for_gpio_ready(value_path)
        self.run_command(f'echo {value} > {value_path}')