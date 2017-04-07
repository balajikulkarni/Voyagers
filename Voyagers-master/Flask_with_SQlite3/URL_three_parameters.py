from flask import Flask,render_template,request
import sqlite3 as sql

app = Flask(__name__)
app.debug = True

sqlite_file = 'PA_GPRS.db'  #DB Name
table = 'Arduino_GPRS'      #Table Name
field = 'GPRS_Data'         #column_name
latitude  = 'Latitude'      #column_name
longitude = 'Longitude'
field_type = 'TEXT'         #Type
coord_type = 'REAL'         #Type


@app.route('/')
def home():
    return 'Hello Voyagers'

@app.route('/gprsdata')
def get_gprsdata():
    #if we are here it means we got a POST on /gprsdata
    name = request.args.get('node')
    lat = request.args.get('lat')
    lng= request.args.get('lng')
    con = sql.connect(sqlite_file)
    try:
        with con:
            c = con.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS {tn}({nf} {ft},{nf1} {ft1},{nf2} {ft2})'\
                      .format(tn=table, nf=field, ft=field_type,
                              nf1=latitude, ft1=coord_type,
                              nf2=longitude, ft2=coord_type))

            c.execute('INSERT INTO {} VALUES (?,?,?)'.format(table),(name,lat,lng))
            con.commit()
            c.close()
        con.close()

        return render_template("main_page.html")

    except Exception:
        return 'Error'
