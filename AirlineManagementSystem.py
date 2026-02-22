import sqlite3
import os

def initialize_db():
    db_file = 'airline.db'
    sql_script = 'AirlineManagementSystem.sql'
   
    db_exists = os.path.exists(db_file)
    
    try:
        conn = sqlite3.connect(db_file)
        if not db_exists:
            if os.path.exists(sql_script):
                with open(sql_script, 'r') as f:
                    conn.executescript(f.read())
                print("Database initialized for the first time.")
            else:
                print("Error: setup.sql file missing!")
        return conn
    except Exception as e:
        print(f"Initialization Error: {e}")
        return None

def check_delays(conn):
    flight_no = input("\nEnter Flight Number: ").strip().upper()
    cursor = conn.cursor()

    query = """
    SELECT f.flight_number, fd.delay_reason, fd.delay_duration_minutes
    FROM Flights f
    JOIN FlightDelays fd ON f.flight_id = fd.flight_id
    WHERE UPPER(f.flight_number) = ?
    """
    cursor.execute(query, (flight_no,))
    results = cursor.fetchall()
    
    if results:
        for r in results:
            print(f"Flight {r[0]}: {r[1]} ({r[2]} mins delay)")
    else:
        print(f"No delay records found for '{flight_no}'.")
def view_flights(conn):
    cursor = conn.cursor()
    query = """
    SELECT f.flight_number, a1.city, a2.city, f.scheduled_departure
    FROM Flights f
    JOIN Airports a1 ON f.origin_airport_id = a1.airport_id
    JOIN Airports a2 ON f.destination_airport_id = a2.airport_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print("\nCURRENT FLIGHT SCHEDULE")
    if not rows:
        print("No flights found. Did you add data to your SQL file?")
    else:
        for row in rows:
            print(f"Flight {row[0]}: {row[1]} to {row[2]} at {row[3]}")
def main():
    conn = initialize_db()
    if not conn:
        return

    try:
        while True:
            print("\nAirline Management System")
            print("1. View Flights")
            print("2. Check Delay")
            print("3. Exit")
            
            choice = input("Select (1-3): ")
            
            if choice == '1':
                view_flights(conn)
            elif choice == '2':
                check_delays(conn)
            elif choice == '3':
                print("Exiting...")
                break
    finally:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()