from classes.google_maps import GoogleMaps
from classes.gps import GPS
from classes.helpers import calculate_relative_direction

start = (38.557963, -121.758756)
curr = (38.557967, -121.758378) # past
# curr = (38.557973, -121.758633) # before
# end = (38.557867, -121.758507) # Right
end = (38.558087, -121.758517) # Left

print(calculate_relative_direction(start[0], start[1], curr[0], curr[1], end[0], end[1]))
# maps = GoogleMaps()
# gps = GPS()

# start = (38.557966, -121.757619)
# end = (38.557803, -121.756577)

# directions = maps.get_directions(start, end)
# print("directions",directions)

# path = maps.directions_to_path(directions)
# print("path", path)

