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

@app.route('/workshop/<id>/<workshopDate>', methods=['GET'])
def getWorkshop(id, workshopDate):
    print(id, workshopDate)
    if workshopDate != 'nearest' and not validateDate(workshopDate):
        return 'bad-request', 400
    
    # workshopDetails = {
    #     'title': 'Fun With Clay',
    #     'shortDescription': "Create beatiful pottery art with your hands, don't worry we are there to help you!",
    #     'duration': '2 Hrs',
    #     'fees': '999/- + GST',
    #     'description': [
    #         'You will get to craft 1 Piece (usually upto 5 inch)',
    #         'You can create Plate, Planter, Mug, Pen Stand or any creative art of your own idea',
    #         'You will get Glazed Product',
    #         'You will receive your final product within 2 weeks',
    #         'If you are multiple people attending workshop, please book separately for each'
    #     ],
    #     'dates': ['Tue, 25 Nov','Wed, 26 Nov','Thu, 27 Nov','Fri, 28 Nov','Sat, 29 Nov','Sun, 30 Nov'],
    #     'selectedDate': 'Wed, 26 Nov',
    #     'availableSlots': ['12PM to 2PM', '2PM to 4PM', '4PM to 6PM', '6PM to 8PM']
    # }

    workshopDetails = getWorkshopDetails(id, workshopDate)
    if workshopDetails is None or workshopDetails == {}:
        return 'not-found', 404
    
    fdates = []
    for date in workshopDetails['dates']:
        dateObj = datetime.strptime(date, '%Y-%m-%d')
        date = dateObj.strftime('%a, %d %b')
        fdates.append(date)
    workshopDetails['dates']=fdates

    fslots = []
    for slot in workshopDetails['availableSlots']:
        if slot['slotsRem'] > 0:
            tm = slot['startTime']
            dtmObj = datetime.fromtimestamp(tm)
            tm = dtmObj.strftime('%I:%M %p')
            fslots.append(tm)
    workshopDetails['availableSlots']=fslots

    fselectedDateObj = datetime.strptime(workshopDetails['selectedDate'], '%Y-%m-%d')
    workshopDetails['selectedDate'] = fselectedDateObj.strftime('%a, %d %b')

    # return workshopDetails
    return render_template('workshop.html', workshopDetails=workshopDetails)

@app.route('/book-workshop', methods=['POST'])
def bookWorkshop():
    if bookWorkshop():
        return "success"
    return "there was an error"

if __name__ == '__main__':
    app.run(debug=True)
