from flask import Flask
import traceback
from flask import request, render_template, url_for
import sqlite3
import time
import json

from logging.config import dictConfig

from workshops import *

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

@app.route('/health-check', methods=['GET'])
def hello():
    return "Everything is Good :)"

@app.route('/workshops', methods=['GET'])
def getWorkshops():
    workshops = getWorkshops()
    return render_template('workshops.html', workshops)

@app.route('/workshop/<id>/<workshopDate>', methods=['GET'])
def getWorkshop(id, workshopDate):
    workshopDetails = getWorkshopDetails(id, workshopDate)
    if workshopDetails is None or workshopDetails == {}:
        return 'not-found', 404
    return render_template('workshop.html', workshopDetails=workshopDetails)

@app.route('/book-workshop', methods=['POST'])
def bookWorkshop():
    if bookWorkshop():
        return "success"
    return "there was an error"

def createWorkshops():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    try:
        res = cur.execute("""
            CREATE TABLE workshops (
                id INTEGER,
                name TEXT,
                description TEXT,
                duration INTEGER,
                fees REAL,
                max_capacity REAL
            )
        """)

        cur.execute("""
            INSERT INTO workshops VALUES
            (1, 'Hand Building', 'workshop-desc', 120, 999.0, 4),
            (2, 'Wheel Building', 'workshop-desc', 120, 1399.0, 4)
        """)
        conn.commit()

        res = cur.execute("SELECT * FROM workshops")
        print(res.fetchall())
    except Exception as e :
        print(e)

def createBookings():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    try:
        res = cur.execute("""
            CREATE TABLE bookings (
                id INTEGER,
                workshop_id INTEGER,
                date_time INTEGER,
                no_of_people INTEGER,
                payment_id TEXT,
                booked_at INTEGER
            )
        """)
        cur.execute("""
            INSERT INTO bookings VALUES
            (1, 1, 1731753000, 2, 'abc-123', 1731771000)
        """)
        conn.commit()

        res = cur.execute("SELECT * FROM bookings")
        print(res.fetchall())
    except Exception as e:
        print(traceback.format_exc())

def createSlots():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    try:
        res = cur.execute("""
            CREATE TABLE slots (
                workshop_id INTEGER,
                date_time INTEGER,
                booked INTEGER
            )
        """)
        cur.execute("""
            INSERT INTO slots VALUES
            (1, 1731857400, 1)
        """)
        conn.commit()

        res = cur.execute("SELECT * FROM slots")
        print(res.fetchall())
    except Exception as e:
        print(traceback.format_exc())


def main():
    print('Starting the application...')
    # createWorkshops()
    # createBookings()
    # createSlots()

main()