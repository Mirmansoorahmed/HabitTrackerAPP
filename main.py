# main.py
import tkinter as tk
from gui import HabitTrackerGUI

if __name__ == "__main__":
    root = tk.Tk()
    habit_tracker_gui = HabitTrackerGUI(root)
    
    # Pre-populate habits
    prepopulated_habits = [
        ("Drink 8 glasses of water", "Daily"),
        ("Exercise for 30 minutes", "Daily"),
        ("Read for 30 minutes", "Daily"),
        ("Clean the house", "Weekly"),
        ("Visit family", "Weekly"),
        ("Pay bills", "Monthly"),
        ("Plan upcoming month", "Monthly"),
        ("Schedule self-care day", "Monthly")
    ]
    for habit_name, frequency in prepopulated_habits:
        habit_tracker_gui.add_prepopulated_habit(habit_name, frequency)
    
    root.mainloop()
