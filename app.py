from flask import Flask
import traceback
from flask import request
import sqlite3
import json

data = {
'workshops': [
    {
        'id': '1',
        'name': 'hand building',
        'details': 'one piece upto 5 inch',
        'duration': '2hrs',
        'fees': 'INR 999 + GST',
        'maxCapacity': 4
    },
    {
        'id': '2',
        'name': 'wheel building',
        'details': 'one piece upto 5 inch',
        'duration': '2hrs',
        'fees': 'INR 1399 + GST',
        'maxCapacity': 4
    }
],
'bookings': [],
'slots': []
}

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return "HELLO WORLD!"

@app.route('/workshops', methods=['GET'])
def getWorkshops():
    pass

@app.route('/workshop/<id>', methods=['GET'])
def getWorkshop():
    pass

@app.route('/book-workshop', methods=['POST'])
def bookWorkshop():
    print(request)
    print(request.url)
    print(request.form['workshop-id'])
    return 'success`'


# @app.route('/workshop-details')
# def getWorkshopDetails():
#     return json.dumps(workshops)

# @app.route('/book-workshop/123')
# def bookWorkshop():
#     workshopId = '1'
#     workshopDate = '20-Nov-2024'
#     workshopTime = '12PM'
#     noOfPeople = '2'
#     if checkSlotAvailibility(workshopId, workshopDate, workshopTime):
#         slots.append({
#             'workshopId': workshopId,
#             'date': workshopDate,
#             'time': workshopTime,
#             'bookedCnt': 1
#         })
#         # process payment
#         paymentId = 'ABC123'
#         bookings.append({
#             'id': 1,
#             'workshopId': workshopId,
#             'workshopDate': workshopDate,
#             'workshopTime': workshopTime,
#             'noOfPeople': noOfPeople,
#             'paymentId': paymentId
#         })
#         return 'Hurray! Your booking is confirmed!'
#     else:
#         return 'Sorry! This slot is just booked, please check other slots.'

# def getMaxCapacity(workshopId):
#     for workshop in workshops:
#         if workshop['id']==workshopId:
#             return workshop['maxCapacity']
#     return -1

# def checkSlotAvailibility(workshopId, date, time):
    isAvailable = True
    for slot in slots:
        if slot['workshopId']==workshopId and slot['date']==date and slot['time']==time:
            if slot['bookedCnt'] >= getMaxCapacity(workshopId):
                isAvailable = False
                break
    return isAvailable

workshops = []
bookings = []
slots = []

def loadData():
    for workshop in data['workshops']:
        workshops.append(workshop)
    for booking in data['bookings']:
        bookings.append(booking)
    for slot in data['slots']:
        slots.append(slot)

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
    createWorkshops()
    createBookings()
    createSlots()

main()