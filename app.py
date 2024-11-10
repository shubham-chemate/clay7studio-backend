from flask import Flask
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

@app.route('/hello')
def hello():
    return "HELLO WORLD!"

@app.route('/workshop-details')
def getWorkshopDetails():
    return json.dumps(workshops)

@app.route('/book-workshop/123')
def bookWorkshop():
    workshopId = '1'
    workshopDate = '20-Nov-2024'
    workshopTime = '12PM'
    noOfPeople = '2'
    if checkSlotAvailibility(workshopId, workshopDate, workshopTime):
        slots.append({
            'workshopId': workshopId,
            'date': workshopDate,
            'time': workshopTime,
            'bookedCnt': 1
        })
        # process payment
        paymentId = 'ABC123'
        bookings.append({
            'id': 1,
            'workshopId': workshopId,
            'workshopDate': workshopDate,
            'workshopTime': workshopTime,
            'noOfPeople': noOfPeople,
            'paymentId': paymentId
        })
        return 'Hurray! Your booking is confirmed!'
    else:
        return 'Sorry! This slot is just booked, please check other slots.'

def getMaxCapacity(workshopId):
    for workshop in workshops:
        if workshop['id']==workshopId:
            return workshop['maxCapacity']
    return -1

def checkSlotAvailibility(workshopId, date, time):
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

def main():
    loadData()

    print(workshops)
    print(bookings)
    print(slots)

main()