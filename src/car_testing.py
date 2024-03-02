from classes.control_system import ConstrolSystem
import time

con = ConstrolSystem(offset=7)

try:
    con.turn()
    print("center")
    time.sleep(1)
    print("slept")
    con.turn(-35)
    print("turned left")
    con.disable_controls()
    print("Stopped")
    time.sleep(1)
    con.turn()
    print("centered")
except Exception as e:
    print(e)
    # print("Sleeping")
    # time.sleep(10)
    # print("Turn")
    # con.turn(-35)
# con.forward(60)
# time.sleep(2)

# con.brake()
# con.turn_center()
# time.sleep(1)

# con.turn(-45)

# time.sleep(1)
# con.turn(45)
# time.sleep(1)



# con.turn_center()
# time.sleep(1)

