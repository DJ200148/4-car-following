from serial import Serial, SerialException
import numpy as np
class GPS:
    def __init__(self, port, baudrate=9600, timeout=1):
        """Initialize GPS connection with a timeout to avoid blocking."""
        try:
            self.gps = Serial(port, baudrate, timeout=timeout)
            self.last_valid_coordinates = (None, None)  # Cache for last known coordinates
        except SerialException as e:
            raise RuntimeError("GPS connection failed") from e

    def _parse_coordinates(self, data):
        """Parse raw NMEA sentence (GPRMC) for latitude and longitude."""
        # Check if valid data is available
        try:
            if data[0] == '$GPRMC' and data[2] == 'A':  # Data[2]: 'A' for valid, 'V' for invalid
                # Parse latitude
                lat_nmea, lat_dir = data[3], data[4]
                lat_deg = float(lat_nmea[:2]) + float(lat_nmea[2:]) / 60
                if lat_dir == 'S':
                    lat_deg *= -1

                # Parse longitude
                lon_nmea, lon_dir = data[5], data[6]
                lon_deg = float(lon_nmea[:3]) + float(lon_nmea[3:]) / 60
                if lon_dir == 'W':
                    lon_deg *= -1

                return (lat_deg, lon_deg)

            return None
        except Exception as error:
            print("problem with parse_coordinates:\n", error)    

    def update(self):
        """Read GPS data and update coordinates."""
        try:
            line = self.gps.readline().decode('utf-8').strip()
            data = line.split(',')
            coords = self._parse_coordinates(data)
            if coords:
                self.last_valid_coordinates = coords
        except SerialException as e:
            print("Error reading GPS data:", e)
        except UnicodeDecodeError:
            print("Error decoding GPS data")
        return self.last_valid_coordinates

    def get_coordinates(self, update=True):
        """Get the last known valid coordinates."""
        if update:
            self.update()
        return self.last_valid_coordinates

    def restart(self):
        """Safely attempt to start the GPS connection if it's not already open."""
        if not self.gps.is_open:
            try:
                self.gps.open()
            except SerialException as e:
                print(f"Failed to open GPS serial connection: {e}")

    def stop(self):
        """Close the GPS connection."""
        self.gps.close()
