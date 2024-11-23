from flask import Flask
from flask import request, render_template, url_for

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
    workshops = getWorkshops_()
    for workshop in workshops:
        workshop['fees'] = 'INR ' + str(workshop['fees']) + '/-'
        fDuration = str(workshop['duration']//60) + " Hrs"
        if workshop['duration']%60 != 0:
            fDuration += " " + str(int(workshop['duration']%60)) + " Mins"
        workshop['duration'] = fDuration
    return render_template('workshops.html', workshops=workshops)

@app.route('/workshop/<id>/<workshopDate>', methods=['GET'])
def getWorkshop(id, workshopDate):
    workshopDetails = getWorkshopDetails(id, workshopDate)
    if workshopDetails is None or workshopDetails == {}:
        return 'not-found', 404
    return workshopDetails
    # return render_template('workshop.html', workshopDetails=workshopDetails)

@app.route('/book-workshop', methods=['POST'])
def bookWorkshop():
    if bookWorkshop():
        return "success"
    return "there was an error"

if __name__ == '__main__':
    app.run(debug=True)
