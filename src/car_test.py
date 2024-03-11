import time

from classes.control_system import ConstrolSystem


sys = ConstrolSystem()
print("Init done")

sys.turn(45)
sys.forward(65)
print("drove")

time.sleep(23.5)
print("slept")

sys.brake()
print("stopped")
sys.turn_center()
print("Done")