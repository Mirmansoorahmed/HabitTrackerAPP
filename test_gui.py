# test_gui.py
import unittest
import tkinter as tk
from unittest.mock import MagicMock
from gui import HabitTrackerGUI

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.gui = HabitTrackerGUI(self.root)

    def test_create_habit_window(self):
        self.gui.create_habit_window()
        self.assertIsInstance(self.gui.habit_name_entry, tk.Entry)
        self.assertIsInstance(self.gui.frequency_dropdown, tk.OptionMenu)

    def test_view_all_habits(self):
        self.gui.view_all_habits()
        # You can add more assertions here based on expected behavior

    def test_show_random_analytics(self):
        self.gui.show_random_analytics()
        # You can add more assertions here based on expected behavior

    def tearDown(self):
        self.root.destroy()

if __name__ == "__main__":
    unittest.main()
