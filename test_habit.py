# test_habit.py
import unittest
from habit import Habit

class TestHabit(unittest.TestCase):
    def setUp(self):
        self.habit = Habit("Test Habit", "Daily")

    def test_init(self):
        self.assertEqual(self.habit.name, "Test Habit")
        self.assertEqual(self.habit.frequency, "Daily")
        self.assertEqual(self.habit.longest_streak, 0)
        self.assertEqual(self.habit.current_streak, 0)
        self.assertEqual(self.habit.completion_rate, 0)

    # Add more test methods for Habit class functionalities

if __name__ == "__main__":
    unittest.main()
