# Airline Management System

A small educational command-line project demonstrating Python, SQLite, relational table design, and SQL joins. It can display a sample flight schedule and show delay records stored in a local database.

**Scope:** this is a local demo using the rows in the SQL setup script. It is not connected to an airline API, does not show live flight status, and does not book tickets.

## Features

- Initialize/ensure the local SQLite schema from the SQL script.
- Display flight numbers, origin and destination cities, and scheduled departure times.
- Search stored delay records by flight number.
- Use parameterized SQL for the user-supplied flight number.
- Enforce SQLite foreign-key checks on the application connection.

## Database design

- **Airports** — airport name, city, and country.
- **Flights** — flight number, origin airport, destination airport, and scheduled departure.
- **FlightDelays** — delay reason and duration linked to a flight.

Primary keys uniquely identify rows. Foreign keys link flights to airports and delay records to flights. The schedule query joins Flights to Airports twice: once for the origin and once for the destination. The delay query joins Flights with FlightDelays.

The SQL setup script uses CREATE TABLE IF NOT EXISTS and INSERT OR IGNORE, so the included sample records are not duplicated when the script is run again. Review the SQL file before using this against any database containing data you care about.

## Requirements

- Python 3.10 or newer
- SQLite support included with Python's sqlite3 module

No third-party Python packages are required.

## Run

Clone or download the repository, then run from the project directory:

```bash
python AirlineManagementSystem.py
```

The program locates the SQL script and database file relative to the Python file, so it does not depend on the terminal's current working directory.

Choose:
1. **View flights** to display the stored schedule.
2. **Check flight delays** and enter a flight number such as E23030.
3. **Exit** to close the database connection.

## Limitations and future improvements

- The repository includes only a small sample schedule and delay record.
- Flight data is static; no live status, ticketing, passenger management, payments, or seat allocation is implemented.
- A production-style version could add input validation for flight creation, passenger/booking tables, transactions, tests, and a documented data-refresh strategy.
