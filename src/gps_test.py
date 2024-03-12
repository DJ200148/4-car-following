from classes.google_maps import GoogleMaps
from classes.gps import GPS
from classes.helpers import calculate_relative_direction

# start = (38.557963, -121.758756)
# curr = (38.557957, -121.758576) # past
# # curr = (38.557973, -121.758633) # before
# # end = (38.557867, -121.758507) # Right
# end = (38.557959, -121.758402) # Left

# print(calculate_relative_direction(start, curr, end))
# maps = GoogleMaps()
gps = GPS()
print(gps.get_coordinates())
# start = (38.557966, -121.757619)
# end = (38.557803, -121.756577)

# directions = maps.get_directions(start, end)
# print("directions",directions)

# path = maps.directions_to_path(directions)
# print("path", path)

