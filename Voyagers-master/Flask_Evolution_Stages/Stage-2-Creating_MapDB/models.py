import sqlite3 as sql
import math
from geopy.geocoders import Nominatim


node = 'NodeName'         #Store NodeName
latitude  = 'Latitude'     #Store Latitude
longitude = 'Longitude'    #Store Longitude
timestamp = 'Timestamp'    #Store Timestamp
pincode = 'Pincode'        #Pincode
text_type = 'TEXT'
real_type = 'REAL'
int_type = 'INT'
time_type = 'TIMESTAMP'


class LocateMe:

    ''' Thanks to Janmatuschek (http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates) for an amazing tutorial on Geolocations'''

    MIN_LAT = math.radians(-90)
    MAX_LAT = math.radians(90)
    MIN_LON = math.radians(-180)
    MAX_LON = math.radians(180)

    #Required to perform distance calculation (kms)
    EARTH_RADIUS = 6378.1

    @classmethod
    def from_degrees(cls, deg_lat, deg_lon):
        rad_lat = math.radians(deg_lat)
        rad_lon = math.radians(deg_lon)
        return LocateMe(rad_lat, rad_lon, deg_lat, deg_lon)

    @classmethod
    def from_radians(cls, rad_lat, rad_lon):
        deg_lat = math.degrees(rad_lat)
        deg_lon = math.degrees(rad_lon)
        return LocateMe(rad_lat, rad_lon, deg_lat, deg_lon)

    @classmethod
    def getAddress(self,coordinates):
        geoLocator = Nominatim()
        location = geoLocator.reverse(coordinates,timeout=5)
        if location is None:
            return 'None'
        return location.address

    def __init__(self,rad_lat,rad_lon,deg_lat,deg_lon):
        self.rad_lat = float(rad_lat)
        self.rad_lon = float(rad_lon)
        self.deg_lat = float(deg_lat)
        self.deg_lon = float(deg_lon)
        self.check_bounds()


    def check_bounds(self):
        if (self.rad_lat < LocateMe.MIN_LAT
            or self.rad_lat > LocateMe.MAX_LAT
            or self.rad_lon < LocateMe.MIN_LON
            or self.rad_lon > LocateMe.MAX_LON):
            return ('Check Bounds Failed:Invalid GeoCoordinates')

    def boundary(self,distance,radius=EARTH_RADIUS):
        if radius < 0 or distance < 0:
            return ('Boundary Failed:Invalid Radius/Distance')

        rad_dist = distance / radius
        min_lat = self.rad_lat - rad_dist
        max_lat = self.rad_lat + rad_dist

        if min_lat > LocateMe.MIN_LAT and max_lat < LocateMe.MAX_LAT:
            delta_lon = math.asin(math.sin(rad_dist) / math.cos(self.rad_lat))

            min_lon = self.rad_lon - delta_lon
            if min_lon < LocateMe.MIN_LON:
                min_lon += 2 * math.pi

            max_lon = self.rad_lon + delta_lon
            if max_lon > LocateMe.MAX_LON:
                max_lon -= 2 * math.pi

        else:
            min_lat = max(min_lat, LocateMe.MIN_LAT)
            max_lat = min(max_lat, LocateMe.MAX_LAT)
            min_lon = LocateMe.MIN_LON
            max_lon = LocateMe.MAX_LON

        return [min_lat,min_lon,max_lat,max_lon]

def Create_DB(sqlite_file,table):
    try:
        con = sql.connect(sqlite_file)
        with con:
            c = con.cursor()
            c.execute('CREATE VIRTUAL TABLE IF NOT EXISTS {tn} USING rtree(NODE_ID,MIN_LATITUDE,MIN_LONGITUDE,MAX_LATITUDE,MAX_LONGITUDE)'
                      .format(tn=table))
            con.commit()
            c.close()
        con.close()

    except Exception:
        if con:
            con.rollback()
        return ('Rolling back DB.Table Creation Failed.')

def InsertInto_DB(sqlite_file,table,data):
    try:
        con = sql.connect(sqlite_file)
        with con:
            c = con.cursor()
            c.execute('INSERT INTO {} VALUES (?,?,?,?,?)'.format(table),(data))
            con.commit()
            c.close()
        con.close()

    except Exception:
        if con:
            con.rollback()
        return ('Rolling back DB.Table Insertion Failed.')
