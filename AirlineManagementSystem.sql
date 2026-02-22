PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Airports (
    airport_id INTEGER PRIMARY KEY,
    airport_name TEXT,
    city TEXT,
    country TEXT
);

CREATE TABLE IF NOT EXISTS Flights (
    flight_id INTEGER PRIMARY KEY,
    flight_number TEXT UNIQUE,
    origin_airport_id INTEGER,
    destination_airport_id INTEGER,
    scheduled_departure TEXT,
    FOREIGN KEY (origin_airport_id) REFERENCES Airports(airport_id),
    FOREIGN KEY (destination_airport_id) REFERENCES Airports(airport_id)
);

CREATE TABLE IF NOT EXISTS FlightDelays (
    delay_id INTEGER PRIMARY KEY,
    flight_id INTEGER,
    delay_reason TEXT,
    delay_duration_minutes INTEGER,
    FOREIGN KEY (flight_id) REFERENCES Flights(flight_id)
);

INSERT OR IGNORE INTO Airports (airport_id, airport_name, city, country) 
VALUES (1, 'Indira Gandhi International', 'Delhi', 'India');

INSERT OR IGNORE INTO Airports (airport_id, airport_name, city, country) 
VALUES (2, 'Chhatrapati Shivaji International', 'Mumbai', 'India');

INSERT OR IGNORE INTO Flights (flight_id, flight_number, origin_airport_id, destination_airport_id, scheduled_departure) 
VALUES (1, 'E23030', 1, 2, '2026-02-21 22:00:00');

INSERT OR IGNORE INTO FlightDelays (flight_id, delay_reason, delay_duration_minutes) 
VALUES (1, 'Technical Glitch', 45);