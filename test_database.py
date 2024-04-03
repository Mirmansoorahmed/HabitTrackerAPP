# test_database.py
import unittest
import sqlite3
from habit import Habit

class TestDatabase(unittest.TestCase):
    def test_create_habit(self):
        habit = Habit("Test Habit", "Daily")
        habit.save_to_database()

        connection = sqlite3.connect("habit_tracker.db")
        cursor = connection.cursor()
        cursor.execute("SELECT name, frequency FROM habits WHERE name=?", ("Test Habit",))
        result = cursor.fetchone()
        connection.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Test Habit")
        self.assertEqual(result[1], "Daily")

    # Add more test methods for database functionalities

if __name__ == "__main__":
    unittest.main()
