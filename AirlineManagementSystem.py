"""Command-line airline schedule and delay viewer backed by SQLite.

This is an educational local database project. It is not connected to live
airline systems and does not book tickets or provide real-time flight status.
"""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "airline.db"
SCHEMA_PATH = BASE_DIR / "AirlineManagementSystem.sql"

def initialize_db():
    """Open the local database and safely ensure its schema/seed rows exist."""
    if not SCHEMA_PATH.is_file():
        print(f"Database setup script not found: {SCHEMA_PATH}")
        return None

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        with SCHEMA_PATH.open("r", encoding="utf-8") as sql_file:
            conn.executescript(sql_file.read())
        return conn
    except (OSError, sqlite3.Error) as exc:
        print(f"Could not initialize the database: {exc}")
        if conn is not None:
            conn.close()
        return None

def view_flights(conn):
    """Display flight routes using joins to the origin/destination airports."""
    query = """
        SELECT f.flight_number,
               origin.city AS origin_city,
               destination.city AS destination_city,
               f.scheduled_departure
        FROM Flights AS f
        JOIN Airports AS origin
          ON origin.airport_id = f.origin_airport_id
        JOIN Airports AS destination
          ON destination.airport_id = f.destination_airport_id
        ORDER BY f.scheduled_departure, f.flight_number
    """
    rows = conn.execute(query).fetchall()

    print("\nFLIGHT SCHEDULE")
    if not rows:
        print("No flights are available in the database.")
        return

    for row in rows:
        print(
            f"{row['flight_number']}: {row['origin_city']} to "
            f"{row['destination_city']} | Departure: {row['scheduled_departure']}"
        )

def check_delays(conn):
    """Find recorded delays for a flight number using a parameterized query."""
    flight_number = input("\nEnter flight number: ").strip().upper()
    if not flight_number:
        print("Flight number cannot be empty.")
        return

    query = """
        SELECT f.flight_number, fd.delay_reason, fd.delay_duration_minutes
        FROM Flights AS f
        JOIN FlightDelays AS fd ON fd.flight_id = f.flight_id
        WHERE UPPER(f.flight_number) = ?
        ORDER BY fd.delay_id
    """
    rows = conn.execute(query, (flight_number,)).fetchall()

    if not rows:
        print(f"No delay records found for '{flight_number}'.")
        return

    for row in rows:
        print(
            f"Flight {row['flight_number']}: {row['delay_reason']} "
            f"({row['delay_duration_minutes']} minutes)"
        )

def main():
    conn = initialize_db()
    if conn is None:
        return

    try:
        while True:
            print("\nAirline Management System")
            print("1. View flights")
            print("2. Check flight delays")
            print("3. Exit")
            choice = input("Select an option (1-3): ").strip()

            try:
                if choice == "1":
                    view_flights(conn)
                elif choice == "2":
                    check_delays(conn)
                elif choice == "3":
                    print("Goodbye.")
                    break
                else:
                    print("Invalid option. Enter 1, 2, or 3.")
            except sqlite3.Error as exc:
                print(f"Database operation failed: {exc}")
    except (EOFError, KeyboardInterrupt):
        print("\nExiting the application.")
    finally:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
