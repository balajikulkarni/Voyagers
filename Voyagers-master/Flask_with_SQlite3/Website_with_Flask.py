from flask import Flask,render_template
import csv
import sqlite3 as sql

app = Flask(__name__)

sqlite_file = 'PA_GPRS.db'  #DB Name
table = 'Arduino_GPRS'      #Table Name
field = 'GPRS_Data'         #column_name
field_type = 'TEXT'         #Type

@app.route('/')
def home():
    return 'Hello Voyagers'

@app.route('/gprsdata')
def get_gprsdata():
    #if we are here it means we got a POST on /gprsdata
    data = str("Testing SQLite")
    con = sql.connect(sqlite_file)
    csvfile = open('addresses.txt', 'r')
    creader = csv.reader(csvfile, delimiter=',')
    with con:
        c = con.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS {tn}({nf} {ft})'\
                  .format(tn=table, nf=field, ft=field_type))
        for data in creader:
            c.execute("INSERT INTO {} VALUES (?)".format(table),(data,))
        con.commit()
        c.close()
    con.close()

    return render_template("main_page.html")
