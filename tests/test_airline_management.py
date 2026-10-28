"""Offline regression tests for the Airline Management System.

Run from the repository root with:
    python -m unittest discover -s tests -v
"""

import contextlib
import io
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import AirlineManagementSystem as airline  # noqa: E402


class AirlineManagementTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.test_root = Path(self.temp_dir.name)
        self.outside_dir = self.test_root / "outside"
        self.outside_dir.mkdir()
        self.db_path = self.test_root / "test_airline.db"
        self.original_db_path = airline.DB_PATH
        self.original_schema_path = airline.SCHEMA_PATH
        airline.DB_PATH = self.db_path
        airline.SCHEMA_PATH = ROOT / "AirlineManagementSystem.sql"
        self.addCleanup(setattr, airline, "DB_PATH", self.original_db_path)
        self.addCleanup(setattr, airline, "SCHEMA_PATH", self.original_schema_path)

    def open_initialized_db(self):
        connection = airline.initialize_db()
        self.assertIsNotNone(connection)
        return connection

    def test_initializes_three_tables_and_sample_rows(self):
        with contextlib.redirect_stdout(io.StringIO()):
            connection = self.open_initialized_db()
        self.addCleanup(connection.close)

        table_names = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
        }
        self.assertEqual(table_names, {"Airports", "Flights", "FlightDelays"})
        self.assertEqual(connection.execute("SELECT COUNT(*) FROM Airports").fetchone()[0], 2)
        self.assertEqual(connection.execute("SELECT COUNT(*) FROM Flights").fetchone()[0], 1)
        self.assertEqual(connection.execute("SELECT COUNT(*) FROM FlightDelays").fetchone()[0], 1)

    def test_repeated_initialization_does_not_duplicate_seed_delay(self):
        with contextlib.redirect_stdout(io.StringIO()):
            first = self.open_initialized_db()
            first.close()
            second = self.open_initialized_db()
        self.addCleanup(second.close)

        self.assertEqual(second.execute("SELECT COUNT(*) FROM FlightDelays").fetchone()[0], 1)

    def test_foreign_keys_are_enabled_and_invalid_reference_is_rejected(self):
        with contextlib.redirect_stdout(io.StringIO()):
            connection = self.open_initialized_db()
        self.addCleanup(connection.close)

        self.assertEqual(connection.execute("PRAGMA foreign_keys").fetchone()[0], 1)
        with self.assertRaises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO Flights (flight_number, origin_airport_id, destination_airport_id) "
                "VALUES ('INVALID', 999, 999)"
            )

    def test_launch_from_other_working_directory(self):
        previous_cwd = Path.cwd()
        try:
            os.chdir(self.outside_dir)
            with contextlib.redirect_stdout(io.StringIO()):
                connection = self.open_initialized_db()
            self.addCleanup(connection.close)
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM Flights").fetchone()[0], 1)
            self.assertTrue(self.db_path.exists())
        finally:
            os.chdir(previous_cwd)

    def test_view_flights_displays_origin_and_destination(self):
        with contextlib.redirect_stdout(io.StringIO()):
            connection = self.open_initialized_db()
        self.addCleanup(connection.close)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            airline.view_flights(connection)

        self.assertIn("Delhi", output.getvalue())
        self.assertIn("Mumbai", output.getvalue())
        self.assertIn("E23030", output.getvalue())

    def test_delay_search_is_case_insensitive(self):
        with contextlib.redirect_stdout(io.StringIO()):
            connection = self.open_initialized_db()
        self.addCleanup(connection.close)

        output = io.StringIO()
        with patch("builtins.input", return_value="e23030"), contextlib.redirect_stdout(output):
            airline.check_delays(connection)

        self.assertIn("Technical Glitch", output.getvalue())
        self.assertIn("45 minutes", output.getvalue())

    def test_empty_flight_number_is_rejected(self):
        with contextlib.redirect_stdout(io.StringIO()):
            connection = self.open_initialized_db()
        self.addCleanup(connection.close)

        output = io.StringIO()
        with patch("builtins.input", return_value=""), contextlib.redirect_stdout(output):
            airline.check_delays(connection)

        self.assertIn("cannot be empty", output.getvalue().lower())


if __name__ == "__main__":
    unittest.main()
