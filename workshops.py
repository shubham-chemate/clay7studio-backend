import sqlite3
import traceback
from datetime import datetime

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

def addUserToDb(name, contact, mail):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()

    try:
        res = cur.execute("""
                        SELECT contact, email
                        FROM USERS
                        WHERE contact=?
                    """, (contact,))
        rows = res.fetchall()
        if len(rows)<=0:
            cur.execute("INSERT INTO USERS VALUES (?, ?, ?)", (name, contact, mail,))
            conn.commit()
            print(f'Inserted user [{name},{contact}] into the database')
        else:
            if len(mail)>0 and rows[0][1]!=mail:
                cur.execute("UPDATE USERS SET email=? WHERE contact=?", (mail, contact,))
                conn.commit()
                print(f'Updating Email from {rows[0][1]} to {mail} for user [{name},{contact}]')
            print(f'User [{name},{contact}] is already in database')
        
        return True
    except Exception as e:
        print(traceback.format_exc())
        return False
    finally:
        conn.close()

def validateWorkshopId(id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    try:
        rows = cur.execute("""
                SELECT id
                FROM workshops
                WHERE id=?
            """,
            (id,)).fetchall()
        if len(rows)<1:
            return False
        return True
    except Exception as e:
        print(traceback.format_exc())
        return False
    finally:
        conn.close()

def checkSlotAvailibility(workshopId, workshopDate, workshopSlot):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    try:
        dtmStr = f'{workshopDate} {workshopSlot}'
        dtmObj = datetime.strptime(dtmStr, "%Y-%m-%d %I:%M %p")
        workshopStartTime = dtmObj.timestamp()
        print(f'Workshop start time is {workshopStartTime}')

        rows = cur.execute("""
                SELECT slotsRem
                FROM SLOTS
                WHERE workshopId=? AND workshopStartTime=?
            """, (workshopId, workshopStartTime,)).fetchall()
        if len(rows)<1 or rows[0][0]<1:
            return False
        
        res = cur.execute("""
                UPDATE SLOTS
                SET slotsRem=slotsRem-1
                WHERE workshopId=? AND workshopStartTime=?
            """, (workshopId, workshopStartTime,)).fetchall()
        conn.commit()

        return True
    except Exception as e:
        print(traceback.format_exc())
        return False
    finally:
        conn.close()

def doPayment():
    return 'placeholder-paymentId'

def addBooking(workshopId, workshopDate, workshopSlot, paymentId, userContact):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    try:
        bookedAt = int(datetime.now().timestamp())        
        res = cur.execute("""
                INSERT INTO BOOKINGS
                VALUES (?,?,?,?,?,?,?)
            """, ('123-abc', workshopId, workshopDate, workshopSlot, paymentId, bookedAt, userContact,)).fetchall()
        conn.commit()

        return True
    except Exception as e:
        print(traceback.format_exc())
        return False
    finally:
        conn.close()

def releaseSlot(workshopId, workshopDate, workshopSlot):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    try:
        dtmStr = f'{workshopDate} {workshopSlot}'
        dtmObj = datetime.strptime(dtmStr, "%Y-%m-%d %I:%M %p")
        workshopStartTime = dtmObj.timestamp()
        print(f'Workshop start time is {workshopStartTime}')

        rows = cur.execute("""
                SELECT slotsRem
                FROM SLOTS
                WHERE workshopId=? AND workshopStartTime=?
            """, (workshopId, workshopStartTime,)).fetchall()
        if len(rows)<1 or rows[0][0]<1:
            return False
        
        res = cur.execute("""
                UPDATE SLOTS
                SET slotsRem=slotsRem+1
                WHERE workshopId=? AND workshopStartTime=?
            """, (workshopId, workshopStartTime,)).fetchall()
        conn.commit()

        return True
    except Exception as e:
        print(traceback.format_exc())
        return False
    finally:
        conn.close()

def bookWorkshop_(workshopDetails):
    userContact = workshopDetails['userContact'].strip()
    userName = workshopDetails['userName'].strip()
    userEmail = workshopDetails['userEmail'].strip()
    workshopId = workshopDetails['workshopId'].strip()
    workshopDate = workshopDetails['workshopDate'].strip()
    workshopSlot = workshopDetails['workshop-slot'].strip()

    if not addUserToDb(userName, userContact, userEmail):
        # return 'server-error', 500
        return False
    
    if not validateWorkshopId(workshopId):
        # return 'invalid workshop id', 400
        return False
    
    if not checkSlotAvailibility(workshopId, workshopDate, workshopSlot):
        # return 'slot not available', 500
        return False
    
    paymentId = doPayment()
    if paymentId is None or paymentId == '':
        if not releaseSlot(workshopId, workshopDate, workshopSlot):
            print(f"some error occured while releasing the slot for [{workshopId},{workshopDate},{workshopSlot}], user [{userName},{userContact},{userEmail}]")
        return False
    else:
        if not addBooking(workshopId, workshopDate, workshopSlot, paymentId, userContact):
            print(f"some error occured while adding record to bookings table for workshop [{workshopId},{workshopDate},{workshopSlot}] ,user [{userName},{userContact},{userEmail}], payementId [{paymentId}]")
        return True