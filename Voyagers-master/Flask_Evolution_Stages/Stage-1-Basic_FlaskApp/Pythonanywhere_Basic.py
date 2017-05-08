
# A very simple Flask Hello World app for you to get started with...

from flask import Flask,render_template
import requests
import sqlite3 as sql

app = Flask(__name__)
db_name = 'GPRS_data'
table = 'Arduino_GPRS'      #Table Name
field = 'GPRS_Data'         #column_name
field_type = 'TEXT'         #Type

@app.route('/gprsdata')
def hello_world():
    r = requests.get('https://www.pythonanywhere.com/user/voyagers/files/home/voyagers/GPRS_TestData.txt')
    data = str(r.text)
    con = sql.connect(db_name)

    with con:
        c = con.cursor();
        c.execute('CREATE TABLE IF NOT EXISTS {tn}({nf} {ft})'\
                  .format(tn=table, nf=field, ft=field_type))
        c.execute("INSERT INTO {} VALUES (?)".format(table),(data,))
        con.commit()
        c.close()

    con.close()

    return render_template("main_page.html")
