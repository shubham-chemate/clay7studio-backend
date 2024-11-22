import traceback
import sqlite3


def createWorkshops():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    try:
        res = cur.execute("""
            CREATE TABLE workshops (
                id TEXT,
                title TEXT,
                shortDescription TEXT,
                duration INTEGER,
                fees REAL,
                max_capacity INTEGER
            )
        """)

        cur.execute("""
            INSERT INTO workshops VALUES
            ('workshop-clay', 'Fun With Clay', 'Create Beautiful Pottery Art Using Clay!', 120, 999.0, 4),
            ('workshop-wheel', 'Fun With Wheel', 'Experience Magic of Wheel and Create Beautiful Pottery Art!', 120, 1399.0, 4),
            ('workshop-clay-and-wheel', 'Fun Together', 'Experience Magic of Hand Clay as well as Wheel Pottery and let your inner article get excited!', 240, 2499.0, 4)
        """)
        conn.commit()

        res = cur.execute("SELECT * FROM workshops")
        print(res.fetchall())
    except Exception as e :
        print(e)

createWorkshops()

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