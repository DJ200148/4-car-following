
from serial import Serial, SerialException
import geopy
from geopy.geocoders import Nominatim
import googlemaps
from dotenv import load_dotenv
import os
import polyline

load_dotenv()  # Loads the .env file

api_key = os.getenv('GOOGLE_API_KEY')

gmaps = googlemaps.Client(key = api_key)
list_lat = []
list_long = []
start = "2063, Davis, CA 95616"
destination = "Silo Market, University of California, Davis, Silo South, Davis, CA 95616"
directions = gmaps.directions(start,destination,mode='walking')
Direction_queue = []
for steps in directions[0]['legs'][0]['steps']:
    line = steps['polyline']['points']
    decode_line = polyline.decode(line, 5)
    print(decode_line)
try:
    gps = Serial('com6',baudrate =9600)
    first = True
    while True:

        unenc_data = gps.readline()
        decodedata = unenc_data.decode("utf-8")
        data = decodedata.split(",")
        if data[0] == '$GPRMC' and data[3] != '' and data[5] != '':

            lat_nmea = data[3]
            lat_degrees = lat_nmea[:2]
            if data[4] == 'S':
                latitude_degrees = float(lat_degrees)*-1
            else:
                latitude_degrees = float(lat_degrees)
            latitude_degrees = str(latitude_degrees).strip('.0')
            lat_ddd = lat_nmea[2:10]
            lat_mmm = float(lat_ddd)/60
            lat_mmm = str(lat_mmm).strip('0.')[:8]
            latitude = latitude_degrees + "." + lat_mmm
            long_nmea = data[5]
            long_degrees = long_nmea[:3]
            if data[6] == 'W':
                longitude_degrees = float(long_degrees)*-1
            else:
                longitude_degrees = float(long_degrees)
            longitude_degrees = str(longitude_degrees).strip('.0')
            long_ddd = long_nmea[3:10]
            long_mmm = float(long_ddd)/60
            long_mmm = str(long_mmm).strip('0.')[:8]
            longitude = longitude_degrees + "." + long_mmm
            if(first):
                print(data)
                print("once")
                first = False
                directions = gmaps.directions(latitude+","+longitude,destination,mode='walking')
                Direction_queue = []
                for steps in directions[0]['legs'][0]['steps']:
                    line = steps['polyline']['points']
                    decode_line = polyline.decode(line, 10)
                    for coor in decode_line:
                        true_coor = tuple(i*100000 for i in coor)
                        Direction_queue.append(true_coor)
                    print(true_coor)
            cur_Long = float(longitude)
            cur_Lat = float(latitude)
            lat_check = abs(cur_Lat - Direction_queue[0][0]) 
            long_check = abs(cur_Long - Direction_queue[0][1])
            print(len(Direction_queue))
            print(Direction_queue[0][0])
            print(lat_check," ",long_check)
            check = 6*10**-5
            print(check)
            if(lat_check <= check and long_check <= check):
                print("yes")
                Direction_queue.pop(0)
            #list_lat.append(lat_check)
            #list_long.append(long_check)
            #print(min(list_lat)," MIN ", min(list_long))
            #print(max(list_lat),"  MAX  ",max(list_long))
            #print(sum(list_lat)/len(list_lat),"  AVG  ",sum(list_long)/len(list_long))
            

except SerialException:
    print("theres no gps connected")
 