from flask import Flask
import json
import data

app = Flask(__name__)

@app.route('/hello')
def hello():
    return "HELLO WORLD!"

@app.route('/workshop-details')
def getWorkshopDetails():
    workshops = [
        {
            "name": "fun with clay(hand building)",
            "duration": "2 Hrs",
            "fees per person": "INR 999",
            "details": "details here"
        },
        {
            "name": "fun with wheel pottery",
            "duration": "2 Hrs",
            "fees per person": "INR 1399",
            "details": 'details here'
        }
    ]

    return json.dumps(workshops)

@app.route('/book-workshop/123')
def bookWorkshop():
    pass

def checkSlotAvailibility(workshopId, date, time):
    pass

workshops = []
bookings = []
slots = []

def loadData():
    for workshop in data.workshops:
        workshops.append(workshop)
    for booking in data.bookings:
        bookings.append(booking)
    for slot in data.slots:
        slots.append(slot)

def main():
    loadData()

    print(workshops)
    print(bookings)
    print(slots)

main()