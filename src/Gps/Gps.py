from serial import Serial, SerialException

class Gps(object):
    #initialize Gps by providing string port and Baudrate of gps device
    def __init__(self,port,baudrate = 9600):
        try:
            self.gps = Serial(port,baudrate)
        except SerialException:
            print("no gps connected or gps is in use already")

    #Update gps coordinates due to gps
    def update(self):
        #to allow cold start time to get fixed sattalites
        calibrate = True
        while(calibrate):
            #reads data on gps
            unenc_data = self.gps.readline()
            #unencodes data
            decodedata = unenc_data.decode("utf-8")
            #turn data into a list
            data = decodedata.split(",")
            #check for if we're getting good data from GPRMC data
            if data[0] == '$GPRMC' and data[3] != '' and data[5] != '':
                #converting our latitutde to decimal
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
                #converting our longitude to decimal
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
                #exit while loop
                calibrate = False
                return latitude, longitude        
