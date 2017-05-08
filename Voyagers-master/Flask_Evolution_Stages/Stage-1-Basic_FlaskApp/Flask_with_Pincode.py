from flask import Flask,render_template,request
from geopy.geocoders import Nominatim
import sqlite3 as sql

app = Flask(__name__)
app.debug = True

sqlite_file = 'PA_GPRS.db'  #DB Name
table = 'Coordinates'      #Table Name
field = 'NodeName'         #column_name
latitude  = 'Latitude'      #column_name
longitude = 'Longitude'
location  = 'Location'
field_type = 'TEXT'         #Type
coord_type = 'REAL'         #Type


@app.route('/')
def home():
    return 'Hello Voyagers'

@app.route('/senddata')
def get_gprsdata():
    #if we are here it means we got a POST on /gprsdata
    name = request.args.get('node')
    lat = request.args.get('lat')
    lng= request.args.get('lng')
    coordinates = lat+","+lng
    loc = str(getAddress(coordinates))
    pincode = loc.split(',')[-2]
    data = (name,lat,lng,pincode)
    con = sql.connect(sqlite_file)

    try:
        with con:
            c = con.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS {tn}({nf} {ft} NOT NULL,{nf1} {ft1} NOT NULL,{nf2} {ft2} NOT NULL,{nf3} {ft3})'\
                      .format(tn=table, nf=field, ft=field_type,
                              nf1=latitude, ft1=coord_type,
                              nf2=longitude,ft2=coord_type,
                              nf3=location, ft3=field_type))

            c.execute('INSERT INTO {} VALUES (?,?,?,?)'.format(table),(data))
            con.commit()
            c.close()
        con.close()

        return render_template("main_page.html")

    except Exception:
        return 'Error:Inserting into Database'



def getAddress(coordinates):
    geoLocator = Nominatim()
    location = geoLocator.reverse(coordinates)
    if location is None:
        return 'Location:None'
    return location.address
