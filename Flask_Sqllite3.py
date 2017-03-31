from flask import Flask, render_template
import requests
import sqlite3 as sql

sqlite_file = 'GPRS.db'
table = 'Arduino_GPRS'      #Table Name
field = 'GPRS_Data'         #column_name
field_type = 'TEXT'         #Type

app = Flask(__name__)

@app.route('/')
def homepage():
    r = requests.get(
                 'http://posttestserver.com/data/2017/03/04/00.00.0168841818')
    data = str(r.text)
    con = sql.connect(sqlite_file)
    with con:
        c = con.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS {tn}({nf} {ft})'\
                  .format(tn=table, nf=field, ft=field_type))
        c.execute("INSERT INTO {} VALUES (?)".format(table),(data,))
        con.commit()
        c.close()
    con.close()

    return r.text

if __name__ == '__main__':
  app.run()
