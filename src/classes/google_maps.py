import googlemaps
from dotenv import load_dotenv
import os
import polyline

from collections import deque
# idea add modes making it possible for the car to go into a circle
class GoogleMaps:
    def __init__(self):
        self.add_coor = (None, None)
        self.Directions = []
        # self.Direction_queue
        try:
            load_dotenv()
            self.api_key = os.getenv('GOOGLE_API_KEY')
            self.gmaps = googlemaps.Client(key = self.api_key)
        except Exception as error:
            print("problem with googlemaps and/or api key \n", error)    

    def get_corrdinates(self, address):
        '''This method will return the coordinates of the address. output: (Lat,Long)'''
        try:
            return self.gmaps.geocode(address)
            # self.add_coor = self.gmaps.geocode(address)
            # return self.add_coor
        except Exception as error:
            print("problem with getting coordinates \n", error)

    def get_directions(self, start, end): 
        '''This method will return the directions from the start to the end. (Lat,Long)'''
        try:
            directions = self.gmaps.directions(start,end,mode ='walking')
            for steps in directions[0]['legs'][0]['steps']:
                line = steps['polyline']['points']
                decode_line = polyline.decode(line)
                for coor in decode_line:
                    self.Directions.append(coor) 
            return self.Directions
        except Exception as error:
            print("problem with get_directions \n", error)    

    def directions_to_path(self, directions): 
        '''This method will return the path from the directions. queue of (Lat,Long)'''
        try:
            return deque(directions)
            # self.Direction_queue = deque(directions)
            # return self.Direction_queue
        except Exception as error:
            print("problem with directions_to_path", error)    
