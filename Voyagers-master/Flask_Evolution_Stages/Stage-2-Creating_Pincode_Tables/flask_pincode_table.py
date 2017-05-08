from flask import Flask,request
from geopy.geocoders import Nominatim
from datetime import datetime
import sqlite3 as sql


app = Flask(__name__)
app.debug = True

field = 'NodeName'         #Store NodeName
latitude  = 'Latitude'     #Store Latitude
longitude = 'Longitude'    #Store Longitude
location = 'Location'      #Store Decoded Location
timestamp = 'Timestamp'    #Store Timestamp
loc_type = 'TEXT'          #Field Type
coord_type = 'REAL'        #Coordinate Type
node_type = 'INT'
time_type = 'TIMESTAMP'


app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
    return 'For the safety of society.We Connect'


@app.route('/senddata',methods=['GET', 'POST'])
def get_gprsdata():
    if request.method == 'GET':
        try:
            node = int(request.args.get('node'))
            lat = request.args.get('lat')
            lng= request.args.get('lng')
            coordinates = lat+','+lng

            #Decode Coordinates
            loc = getAddress(coordinates)
            if loc is 'None':
                return 'Unable to GeoLocate Coordinates!'

            #TBD : Better Logic to create table name
            pincode = loc.split(',')[-2]
            table = str('PIN_'+pincode).replace(" ","")
            city = loc.split(',')[-4].upper()
            sqlite_file = ''.join((city,'.db'))

            #Create location to be stored
            loc = ''.join(map(str,loc))

            #Insert Timestamp as well
            date= str(datetime.now())
            date = ''.join(map(str,date))

            #Final 'data' that goes into DB
            data = (node,lat,lng,loc,date)

        except Exception:
            return ('Data Preparation Error')

        try:
            con = sql.connect(sqlite_file)
            with con:
                c = con.cursor()
                c.execute('CREATE TABLE IF NOT EXISTS {tn}({nf} {ft},{nf1} {ft1},{nf2} {ft2},{nf3} {ft3},{nf4} {ft4})'\
                          .format(tn =table ,nf=field, ft=node_type,
                                  nf1=latitude,ft1=coord_type,
                                  nf2=longitude,ft2=coord_type,
                                  nf3=location,ft3=loc_type,
                                  nf4=timestamp,ft4=loc_type))

                c.execute('INSERT INTO {} VALUES (?,?,?,?,?)'.format(table),(data))
                con.commit()
                c.close()
            con.close()

        except Exception:
            if con:
                con.rollback()
            return ('Table Creation/Insertion Error')

        return ('Stored Successfully Into %s Table of %s Database') % (pincode,city)
    else:
        return 'GET Not handled!'

def getAddress(coordinates):
    geoLocator = Nominatim()
    location = geoLocator.reverse(coordinates)
    if location is None:
        return 'None'
    return location.address