CREATE TABLE workshops (
    id INTEGER,
    name TEXT,
    description TEXT,
    duration INTEGER,
    fees REAL,
    max_capacity INTEGER
)

INSERT INTO workshops VALUES
(1, 'Hand Building', 'workshop-desc', 120, 999.0, 4),
(2, 'Wheel Building', 'workshop-desc', 120, 1399.0, 4)


CREATE TABLE bookings (
    id INTEGER,
    workshop_id INTEGER,
    date_time INTEGER,
    no_of_people INTEGER,
    payment_id TEXT,
    booked_at INTEGER,
)

INSERT INTO bookings VALUES
(1, 1, 1731753000, 2, 'abc-123', 1731771000)

CREATE TABLE slots (
    workshop_id INTEGER,
    date_time INTEGER,
    booked INTEGER
)

INSERT INTO slots VALUES
(1, 1731857400, 1)