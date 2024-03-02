from classes.control_system import ConstrolSystem
import time

con = ConstrolSystem(offset=7)
time.sleep(1)
con.turn(-35)
# con.forward(60)
# time.sleep(2)

con.brake()
# con.turn_center()
# time.sleep(1)

# con.turn(-45)

# time.sleep(1)
# con.turn(45)
# time.sleep(1)



# con.turn_center()
# time.sleep(1)

