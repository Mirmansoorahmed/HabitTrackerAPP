# gui.py
import tkinter as tk
from tkinter import messagebox
from habit import Habit
import sqlite3
import random

class HabitTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("800x600")  # Set initial window size
        self.root.iconbitmap("icon.ico")  # Set application icon

        self.create_database()

        self.label = tk.Label(root, text="Ready For Habit Tracking", font=("Arial", 20))
        self.label.pack(pady=30)

        self.create_button = tk.Button(root, text="Create New Habit", command=self.create_habit_window, font=("Arial", 12))
        self.create_button.pack(pady=15)

        self.view_all_button = tk.Button(root, text="View All Habits", command=self.view_all_habits, font=("Arial", 12))
        self.view_all_button.pack(pady=15)

        self.analytics_button = tk.Button(root, text="Track Your Habits", command=self.show_random_analytics, font=("Arial", 12))
        self.analytics_button.pack(pady=15)

    def create_database(self):
        connection = sqlite3.connect("habit_tracker.db")
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS habits (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            frequency TEXT NOT NULL,
                            longest_streak INTEGER DEFAULT 0,
                            current_streak INTEGER DEFAULT 0,
                            completion_rate REAL DEFAULT 0
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS habit_logs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            habit_id INTEGER NOT NULL,
                            date DATE NOT NULL,
                            completed INTEGER NOT NULL,
                            FOREIGN KEY (habit_id) REFERENCES habits(id)
                        )''')
        connection.commit()
        connection.close()

    def add_prepopulated_habit(self, name, frequency):
        habit = Habit(name, frequency)
        habit.save_to_database()

    def create_habit_window(self):
        habit_window = tk.Toplevel(self.root)
        habit_window.title("Create New Habit")

        tk.Label(habit_window, text="Habit Name:", font=("Arial", 12)).pack(pady=10)
        self.habit_name_entry = tk.Entry(habit_window, font=("Arial", 12))
        self.habit_name_entry.pack(pady=5)

        tk.Label(habit_window, text="Frequency:", font=("Arial", 12)).pack(pady=10)
        self.frequency_var = tk.StringVar(habit_window)
        self.frequency_var.set("Daily")  # Default value
        frequencies = ["Daily", "Weekly", "Monthly"]
        self.frequency_dropdown = tk.OptionMenu(habit_window, self.frequency_var, *frequencies)
        self.frequency_dropdown.config(font=("Arial", 12))
        self.frequency_dropdown.pack(pady=5)

        create_button = tk.Button(habit_window, text="Create Habit", command=self.create_habit, font=("Arial", 12))
        create_button.pack(pady=10)

    def create_habit(self):
        name = self.habit_name_entry.get()
        frequency = self.frequency_var.get()
        if name:
            habit = Habit(name, frequency)
            habit.save_to_database()
            messagebox.showinfo("Success", "Habit created successfully!")
        else:
            messagebox.showerror("Error", "Please enter a habit name.")

    def view_all_habits(self):
        all_habits_window = tk.Toplevel(self.root)
        all_habits_window.title("All Habits")

        connection = sqlite3.connect("habit_tracker.db")
        cursor = connection.cursor()
        cursor.execute("SELECT name, completion_rate FROM habits")
        habits = cursor.fetchall()
        connection.close()

        for habit in habits:
            habit_label = tk.Label(all_habits_window, text=f"Habit: {habit[0]}, Completion Rate: {habit[1]}%", font=("Arial", 12))
            habit_label.pack(pady=5)

    def show_random_analytics(self):
        connection = sqlite3.connect("habit_tracker.db")
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM habits")
        habits = cursor.fetchall()
        connection.close()

        if habits:
            random_habit = random.choice(habits)[0]
            habit = Habit(random_habit, "")  # Dummy habit object, frequency not required for analytics
            habit.update_analytics()
            self.view_analytics(habit)
        else:
            messagebox.showerror("Error", "No habits found to show analytics.")

    def view_analytics(self, habit):
        analytics_window = tk.Toplevel(self.root)
        analytics_window.title("Habit Analytics")

        habit_label = tk.Label(analytics_window, text=f"Habit: {habit.name}", font=("Arial", 16))
        habit_label.pack(pady=10)

        longest_streak_label = tk.Label(analytics_window, text=f"Longest Streak: {habit.longest_streak}", font=("Arial", 12))
        longest_streak_label.pack()

        current_streak_label = tk.Label(analytics_window, text=f"Current Streak: {habit.current_streak}", font=("Arial", 12))
        current_streak_label.pack()

        completion_rate_label = tk.Label(analytics_window, text=f"Completion Rate: {habit.completion_rate}%", font=("Arial", 12))
        completion_rate_label.pack()
