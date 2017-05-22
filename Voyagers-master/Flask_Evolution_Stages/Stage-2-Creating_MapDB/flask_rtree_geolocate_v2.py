from flask import Flask,request
from datetime import datetime
from models import LocateMe,Create_DB,InsertInto_DB,SelectFrom_DB

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
            alarm = request.args.get('alarm')
            coordinates = lat+','+lng
        except Exception:
            return ('Insufficient/Invalid URL Parameters')


        #Decode Coordinates
        address = LocateMe.getAddress(coordinates)
        if address is 'None':
            return 'Reverse Geolocate :NONE'


        #[TBD] Better Logic to create table name
        #pincode = address.split(',')[-2]
        #table = str('PIN_'+pincode).replace(" ","")

        table = 'Userdata'
        city = address.split(',')[-4].upper()
        sqlite_file = ''.join((city,'.db'))

        #Insert Timestamp as well
        date= str(datetime.now())
        date = ''.join(map(str,date))

        #Scan Radius in KM
        distance = 3
        lat = float(lat)
        lng = float(lng)

        lat,lng = LocateMe.convert_to_radians(lat,lng)
        data = (node,lat,lng)

        Create_DB(sqlite_file,table)
        InsertInto_DB(sqlite_file,table,data)

        loc = LocateMe.from_degrees(lat,lng)


        if alarm == '1':
            #MayDay!, Time to signal the Knights
            min_lat,min_lng,max_lat,max_lng = loc.boundary(distance)
            boundaries = [min_lat,min_lng,max_lat,max_lng]
            rc = SelectFrom_DB(sqlite_file,table,lat,lng,boundaries,distance)

            #TBD:If we hit None,should re-queue the query with larger raduis??
            if rc != 'None':
                return ('Notified %s node-details to the Knights Watch') % (node)
            else:
                return ('No one found nearby :(')
        else:
            #Sync Request
            return ('Stored Successfully Into %s Table of %s Database') % (table,city)

    else:
        return 'GET Not handled!'
