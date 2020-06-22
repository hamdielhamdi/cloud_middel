
from flask import Flask, request
import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import datetime


app = Flask(__name__)


def create_db_table():
    """ check connection if treu pass , else create data base + empty table"""

    
    try:
        con = sqlite3.connect('file:requests.db?mode=rw', uri=True)
        con.close()
    except Exception as e:
        engine = create_engine('sqlite:///requests.db', echo=True)
        meta = MetaData()
        students = Table(
            'requests', meta,
            Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('url', String),
            Column('datec', String)
    
        )
        meta.create_all(engine)


def insert_data_in_db(url, date):
    # handle db 
    create_db_table()

    # conenct and insert data 
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    # for test perpose todo : change to sqlalchamy query
    c.execute("INSERT INTO REQUESTS (URL, datec) VALUES ('{}','{}')".format(url, date))
    conn.commit()
    conn.close()


@app.route('/insert', methods=['GET', 'POST'])
def bridge_insert():
    # get json payload
    r = request.get_json()
    print(r)

    # if ok insert 
    insert_data_in_db(r['url'], datetime.datetime.now())

    return str({'text': 'Your request is being processed'}), 200


@app.route('/query')
def bridge_get():
    conn = sqlite3.connect('requests.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests")

    rows = cur.fetchall()

    data = []
    for row in rows:
        data.append(row)
    conn.close()
    return str(data), 200





if __name__ == "__main__":
   #app.run() ##Replaced with below code to run it using waitress
   serve(app, host='0.0.0.0', port=5000)