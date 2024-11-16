from flask import Flask
import traceback
from flask import request
import sqlite3
import time
import json

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return "HELLO WORLD!"

@app.route('/workshops', methods=['GET'])
def getWorkshops():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        res = cur.execute("SELECT id, name, description, duration, fees, max_capacity FROM WORKSHOPS")
        rows = res.fetchall()
        workshops = [dict(row) for row in rows]
        return workshops
    except Exception as e:
        print(traceback.format_exc())
        return 'server-error', 500
    finally:
        conn.close()

@app.route('/workshop/<id>', methods=['GET'])
def getWorkshop(id):
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        res = cur.execute("SELECT id, name, description, duration, fees, max_capacity FROM WORKSHOPS WHERE id=?", (id,))
        rows = res.fetchall()
        workshops = [dict(row) for row in rows]
        if len(workshops)>0:
            return workshops[0]
        return {}
    except Exception as e:
        print(traceback.format_exc())
        return 'server-error', 500
    finally:
        conn.close()

@app.route('/book-workshop', methods=['POST'])
def bookWorkshop():
    workshop_id = request.form['workshop-id']
    slot_datetime = request.form['slot-datetime']
    no_of_people = request.form['no_of_people']

    if workshop_id is None:
        return 'please provide workshop-id', 400
    if slot_datetime is None:
        return 'please provide slot-datetime', 400
    if no_of_people is None:
        return 'please provide no-of-people', 400

    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    
    rows = cur.execute("""
            SELECT max_capacity
            FROM workshops
            WHERE id=?
        """,
        (workshop_id)).fetchall()
    if len(rows)<1:
        conn.close()
        return 'workshop-id is not present in database', 400
    
    max_capacity = int(rows[0][0])

    rows = cur.execute("""
            SELECT booked
            FROM slots
            WHERE workshop_id=? AND date_time=?
        """,
        (workshop_id, slot_datetime)).fetchall()

    if len(rows)<1:
        conn.close()
        return 'no slot present for workshop id: '+workshop_id, 400
    
    booked = int(rows[0][0])

    if booked>=max_capacity:
        conn.close()
        return "no-slots-left for workshop id: " + workshop_id
    
    cur.execute("""
            UPDATE slots
            SET booked=booked+1
            WHERE workshop_id=? AND date_time=?
        """,
        (workshop_id, slot_datetime))
    
    conn.commit()

    def doPayment():
        tl=30
        print(f'Please complete your payment within {tl} secs')
        time.sleep(tl)
        import random
        n = random.choice([0,1])
        if n==0:
            print("Payment Failure")
            return False
        else:
            print("Payment Success")
            return True

    if doPayment():
        cur.execute("""
                INSERT INTO bookings
                VALUES (1,?,?,?,'abc-123',1234)
            """,
            (workshop_id, slot_datetime,no_of_people))
        conn.commit()
        conn.close()
        return 'booked-successfully'
    else:
        cur.execute("""
            UPDATE slots
            SET booked=booked-1
            WHERE workshop_id=? AND date_time=?
        """,
        (workshop_id, slot_datetime))
    
        conn.commit()
        conn.close()
        return 'payment-failure'

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