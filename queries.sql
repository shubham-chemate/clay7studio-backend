CREATE TABLE workshops (
    id TEXT,
    title TEXT,
    shortDescription TEXT,
    duration INTEGER,
    fees INTEGER,
    maxCapacity INTEGER
)

INSERT INTO workshops VALUES
('workshop-clay', 'Fun With Clay', 'Create Beautiful Pottery Art Using Clay!', 120, 999, 4),
('workshop-wheel', 'Fun With Wheel', 'Experience Magic of Wheel and Create Beautiful Pottery Art!', 120, 1399, 4),
('workshop-clay-and-wheel', 'Fun Together', 'Experience Magic of Hand Clay as well as Wheel Pottery and let your inner article get excited!', 240, 2499, 4)


CREATE TABLE WORKSHOP_DESC (
    workshopId TEXT,
    workshopDesc TEXT,
    displayPriority INTEGER
)

INSERT INTO WORKSHOP_DESC VALUES
('workshop-clay', 'You will get to craft 1 Piece (usually upto 5 inch) using the magic of your hand!', 1),
('workshop-clay', 'You can create Plate, Planter, Mug, Pen Stand or any creative art of your own idea', 2),
('workshop-clay', 'You will get Glazed Product', 3),
('workshop-clay', 'You will receive your final product within 2 weeks', 4),
('workshop-clay', 'If you are multiple people attending workshop, please book separately for each',5),
('workshop-wheel', 'Create your art on wheel - Exclusive wheel pottery!', 1),
('workshop-wheel', 'You will be able to craft 1 Piece (usually upto 5 inch)', 2),
('workshop-wheel', 'You can create Plate, Planter, Mug, Pen Stand or any creative art of your own idea', 3),
('workshop-wheel', 'You will get Glazed Product', 4),
('workshop-wheel', 'You will receive your final product within 2 weeks', 5),
('workshop-wheel', 'If you are multiple people attending workshop, please book separately for each', 6),
('workshop-clay-and-wheel', 'Get deep dive into pottery art with hand and wheel pottery', 1),
('workshop-clay-and-wheel', 'You will be able to create 2 arts - one with your hand and other on a wheel', 2),
('workshop-clay-and-wheel', 'You will receive your final product within 2 weeks', 3),
('workshop-clay-and-wheel', 'If you are multiple people attending workshop, please book separately for each', 4)

SELECT workshopDesc
FROM WORKSHOP_DESC
WHERE workshopId='workshop-clay'
ORDER BY displayPriority

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


SELECT max_capacity, booked
FROM workshops w
INNER JOIN slots s ON w.id = s.workshop_id
WHERE w.id=1