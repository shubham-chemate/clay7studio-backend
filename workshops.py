import sqlite3
import traceback

def getWorkshops_():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        res = cur.execute("SELECT id, title, shortDescription, duration, fees FROM WORKSHOPS")
        cols = [desc[0] for desc in res.description]
        rows = res.fetchall()
        workshops = [dict(zip(cols, row)) for row in rows]
        return workshops
    except Exception as e:
        print(traceback.format_exc())
        return 'server-error', 500
    finally:
        conn.close()

def getWorkshopDetails(id, workshopDate):
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        res = cur.execute("SELECT id, title, shortDescription, duration, fees FROM WORKSHOPS WHERE id=?", (id,))
        rows = res.fetchall()
        workshops = [dict(row) for row in rows]

        if len(workshops)<=0:
            return {}

        workshop = workshops[0]

        res = cur.execute("SELECT workshopDesc FROM WORKSHOP_DESC WHERE workshopId=? ORDER BY displayPriority", (id,))
        rows = res.fetchall()
        desc = [row[0] for row in rows]

        if len(desc)>0:
            workshop['description']=desc

        return workshop
    except Exception as e:
        print(traceback.format_exc())
        return 'server-error', 500
    finally:
        conn.close()


    return {
        'title': 'Fun With Clay',
        'shortDescription': "Create beatiful pottery art with your hands, don't worry we are there to help you!",
        'duration': '2 Hrs',
        'fees': '999/- + GST',
        'description': [
            'You will get to craft 1 Piece (usually upto 5 inch)',
            'You can create Plate, Planter, Mug, Pen Stand or any creative art of your own idea',
            'You will get Glazed Product',
            'You will receive your final product within 2 weeks',
            'If you are multiple people attending workshop, please book separately for each'
        ],
        'dates': ['Tue, 25 Nov','Wed, 26 Nov','Thu, 27 Nov','Fri, 28 Nov','Sat, 29 Nov','Sun, 30 Nov'],
        'selectedDate': 'Wed, 26 Nov',
        'availableSlots': ['12PM to 2PM', '2PM to 4PM', '4PM to 6PM', '6PM to 8PM']
    }
    # return {}

def bookWorkshop():
        # workshop_id = request.form['workshop-id']
    # slot_datetime = request.form['slot-datetime']
    # no_of_people = request.form['no_of_people']

    # if workshop_id is None:
    #     return 'please provide workshop-id', 400
    # if slot_datetime is None:
    #     return 'please provide slot-datetime', 400
    # if no_of_people is None:
    #     return 'please provide no-of-people', 400

    # conn = sqlite3.connect("data.db")
    # cur = conn.cursor()
    
    # rows = cur.execute("""
    #         SELECT max_capacity
    #         FROM workshops
    #         WHERE id=?
    #     """,
    #     (workshop_id)).fetchall()
    # if len(rows)<1:
    #     conn.close()
    #     return 'workshop-id is not present in database', 400
    
    # max_capacity = int(rows[0][0])

    # rows = cur.execute("""
    #         SELECT booked
    #         FROM slots
    #         WHERE workshop_id=? AND date_time=?
    #     """,
    #     (workshop_id, slot_datetime)).fetchall()

    # if len(rows)<1:
    #     conn.close()
    #     return 'no slot present for workshop id: '+workshop_id, 400
    
    # booked = int(rows[0][0])

    # if booked>=max_capacity:
    #     conn.close()
    #     return "no-slots-left for workshop id: " + workshop_id
    
    # cur.execute("""
    #         UPDATE slots
    #         SET booked=booked+1
    #         WHERE workshop_id=? AND date_time=?
    #     """,
    #     (workshop_id, slot_datetime))
    
    # conn.commit()

    # def doPayment():
    #     tl=30
    #     print(f'Please complete your payment within {tl} secs')
    #     time.sleep(tl)
    #     import random
    #     n = random.choice([0,1])
    #     if n==0:
    #         print("Payment Failure")
    #         return False
    #     else:
    #         print("Payment Success")
    #         return True

    # if doPayment():
    #     cur.execute("""
    #             INSERT INTO bookings
    #             VALUES (1,?,?,?,'abc-123',1234)
    #         """,
    #         (workshop_id, slot_datetime,no_of_people))
    #     conn.commit()
    #     conn.close()
    #     return 'booked-successfully'
    # else:
    #     cur.execute("""
    #         UPDATE slots
    #         SET booked=booked-1
    #         WHERE workshop_id=? AND date_time=?
    #     """,
    #     (workshop_id, slot_datetime))
    
    #     conn.commit()
    #     conn.close()
    #     return 'payment-failure'
    return "booked"