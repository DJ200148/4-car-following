from classes.control_system import ConstrolSystem
import time

con = ConstrolSystem(offset=7)

try:
    con.turn(-35)
    print("turned left")
    time.sleep(2)

    con.disable_controls()
    print("Stopped")
    time.sleep(2)
    
    con.turn()
    print("tried to go centered")
    time.sleep(2)

    # con.enable_controls()
    # print("Enabled")
    # time.sleep(2)

    con.turn(35)
    print("turned right")
    time.sleep(2)
    
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

