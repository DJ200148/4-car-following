from classes.control_system import ConstrolSystem
from time import sleep


control_system = ConstrolSystem()
# Create a list of functions to call in the loop
functions_to_call = [
    # control_system.forward,
    # control_system.reverse,
    # control_system.brake,
    # control_system.turn_center,
    control_system.turn_left,
    control_system.turn_right
]

# test each functions 
while True:
    for function in functions_to_call:
        function()  # this calls the function defined above
        sleep(5)