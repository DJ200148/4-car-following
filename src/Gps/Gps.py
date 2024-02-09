from serial import Serial, SerialException

class Gps(object):
    def __init__(self,port,baudrate = 9600):
        self.gps = Serial(port,baudrate)
        self.latitude = ""
        self.longitude = ""

    def update(self):
        calibrate = True
        while(calibrate):
            unenc_data = self.gps.readline()
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
                calibrate = False
                return latitude, longitude        
