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

        res = cur.execute("""
                        SELECT distinct date(workshopStartTime, 'unixepoch', '+0 hours', 'localtime') as workshopTime 
                        FROM SLOTS 
                        WHERE workshopId=? and workshopStartTime > strftime('%s', 'now', 'start of day', '+0 hours', 'localtime')
                        LIMIT 6;
                    """, (id,))
        rows = res.fetchall()
        dates = [row[0] for row in rows]
        workshop['dates']=dates
        if len(dates)<=0:
            return workshop

        if workshopDate == "nearest":
            workshopDate = dates[0]

        workshop['selectedDate']=workshopDate

        res = cur.execute("""
            select workshopStartTime, slotsRem
            from slots
            where workshopId=? and date(workshopStartTime, 'unixepoch', '+0 hours', 'localtime') = ?;
        """, (id, workshopDate,))
        rows = res.fetchall()
        slots=[dict(zip(['startTime', 'slotsRem'], row)) for row in rows]
        workshop['availableSlots']=slots

        return workshop
    except Exception as e:
        print(traceback.format_exc())
        return 'server-error', 500
    finally:
        conn.close()

    return {}

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