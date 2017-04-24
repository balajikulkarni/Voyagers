from flask import Flask,render_template,request
import sqlite3 as sql

app = Flask(__name__)
app.debug = True

sqlite_file = 'PA_GPRS.db'  #DB Name
table = 'Coordinates'      #Table Name
field = 'NodeName'         #column_name
latitude  = 'Latitude'      #column_name
longitude = 'Longitude'
field_type = 'TEXT'         #Type
coord_type = 'REAL'         #Type


@app.route('/')
def home():
    return 'Hello Voyagers'

@app.route('/senddata',methods=['GET', 'POST'])
def get_gprsdata():
    if request.method == 'POST':
        name = request.args.get('node')
        lat = request.args.get('lat')
        lng= request.args.get('lng')
        data = (name,lat,lng)
        con = sql.connect(sqlite_file)

        with con:
            c = con.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS {tn}({nf} {ft},{nf1} {ft1},{nf2} {ft2})'\
                      .format(tn=table, nf=field, ft=field_type,
                              nf1=latitude, ft1=coord_type,
                              nf2=longitude, ft2=coord_type))
            c.execute('INSERT INTO {} VALUES (?,?,?)'.format(table),(data))
            con.commit()
            c.close()
        con.close()

        #return render_template("main_page.html")
        return str(data)

    else:
        #return render_template("get_page.html")
        return 'GET Not handled for now!'
