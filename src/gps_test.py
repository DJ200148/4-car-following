from classes.google_maps import GoogleMaps
from classes.gps import GPS

maps = GoogleMaps()
# gps = GPS()

start = (38.557966, -121.757619)
end = (38.557803, -121.756577)

directions = maps.get_directions(start, end)
print("directions",directions)

path = maps.directions_to_path(directions)
print("path", path)

