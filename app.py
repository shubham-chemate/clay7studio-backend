from flask import Flask
from flask import request, render_template, url_for

from logging.config import dictConfig
from datetime import datetime

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
    workshops = getWorkshops_()
    for workshop in workshops:
        workshop['fees'] = 'INR ' + str(workshop['fees']) + '/-'
        fDuration = str(workshop['duration']//60) + " Hrs"
        if workshop['duration']%60 != 0:
            fDuration += " " + str(int(workshop['duration']%60)) + " Mins"
        workshop['duration'] = fDuration
    return render_template('workshops.html', workshops=workshops)

# YYYY-MM-DD
def validateDate(date):
    try:
        [y, m, d] = date.split('-')
        if int(y)>=2024 and int(y)<=2050 and int(m)>=1 and int(m)<=12 and int(d)>=1 and int(d)<=31:
            return True
    except Exception as e:
        print(e)
    return False

# 2024-11-23 -> Sat, 23 Nov
@app.template_filter('formatDate')
def formatDate(date):
    dateObj = datetime.strptime(date, '%Y-%m-%d')
    date = dateObj.strftime('%a, %d %b')
    return date

@app.route('/workshop/<id>/<workshopDate>', methods=['GET'])
def getWorkshop(id, workshopDate):
    print(id, workshopDate)
    if workshopDate != 'nearest' and not validateDate(workshopDate):
        return 'bad-request', 400

    workshopDetails = getWorkshopDetails(id, workshopDate)
    if workshopDetails is None or workshopDetails == {}:
        return 'not-found', 404
    
    workshopDetails['fees'] = 'INR '+str(workshopDetails['fees'])+'/-'
    
    fDuration = str(workshopDetails['duration']//60) + " Hrs"
    if workshopDetails['duration']%60 != 0:
        fDuration += " " + str(int(workshopDetails['duration']%60)) + " Mins"
    workshopDetails['duration'] = fDuration

    fslots = []
    for slot in workshopDetails['availableSlots']:
        if slot['slotsRem'] > 0:
            tm = slot['startTime']
            dtmObj = datetime.fromtimestamp(tm)
            tm = dtmObj.strftime('%I:%M %p')
            fslots.append(tm)
    workshopDetails['availableSlots']=fslots

    # return workshopDetails
    return render_template('workshop.html', workshopDetails=workshopDetails)

@app.route('/book-workshop', methods=['POST'])
def bookWorkshop():
    userContact = request.form['userContact']
    userName = request.form['userName']
    userEmail = request.form['userEmail']
    workshopId = request.form['workshopId']
    workshopDate = request.form['workshopDate']
    workshopSlot = request.form['workshop-slot']

    if userContact is None or userContact == '':
        return 'No user contact is given', 400
    if userName is None or userName == '':
        return 'No username is given', 400
    if workshopId is None or workshopId == '':
        return 'WorkshopId is not present', 400
    if workshopDate is None or workshopDate == '':
        return 'WorkshopDate is not present', 400
    if workshopSlot is None or workshopSlot == '':
        return 'WorkshopSlot is not present', 400

    if bookWorkshop_(request.form):
        return "booked-successfully"
    return "booking failed"

if __name__ == '__main__':
    app.run(debug=True)
