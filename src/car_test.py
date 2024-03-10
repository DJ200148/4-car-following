import time

from classes.control_system import ConstrolSystem


sys = ConstrolSystem()
print("Init done")


sys.forward(60)
print("drove")

time.sleep(5)
print("slept")

sys.brake()
print("stopped")

time.sleep(2)
sys.turn_center()
print("Done")