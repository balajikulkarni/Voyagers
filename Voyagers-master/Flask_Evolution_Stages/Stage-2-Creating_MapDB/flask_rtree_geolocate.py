from flask import Flask,request
from datetime import datetime
from models import LocateMe,Create_DB,InsertInto_DB

app = Flask(__name__)
app.debug = True


@app.route('/')
def home():
    return 'Connectivity leads to Safety.'


@app.errorhandler(404)
def not_found(error):
    return '404:Not Found'

@app.route('/senddata',methods=['GET', 'POST'])
def get_gprsdata():
    if request.method == 'GET':
        try:
            node = int(request.args.get('node'))
            lat = request.args.get('lat')
            lng = request.args.get('lng')
            coordinates = lat+','+lng
        except Exception:
            return ('Insufficient/Invalid URL Parameters')


        #Decode Coordinates
        address = LocateMe.getAddress(coordinates)
        if address is 'None':
            return 'Reverse Geolocate :NONE'


        #[TBD] Better Logic to create table name
        pincode = address.split(',')[-2]
        table = str('PIN_'+pincode).replace(" ","")
        city = address.split(',')[-4].upper()
        sqlite_file = ''.join((city,'.db'))

        #Insert Timestamp as well
        date= str(datetime.now())
        date = ''.join(map(str,date))

        #Radius to scan in KM
        distance = 1.5
        lat = float(lat)
        lng = float(lng)
        loc = LocateMe.from_degrees(lat,lng)
        min_lat,min_lng,max_lat,max_lng = loc.boundary(distance)

        data = (node,min_lat,min_lng,max_lat,max_lng)


        Create_DB(sqlite_file,table)
        InsertInto_DB(sqlite_file,table,data)

        return ('Stored Successfully Into %s Table of %s Database') % (pincode,city)

    else:
        return 'GET Not handled!'
