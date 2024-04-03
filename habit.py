# habit.py
import sqlite3
import datetime

class Habit:
    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency
        self.longest_streak = 0
        self.current_streak = 0
        self.completion_rate = 0

    def save_to_database(self):
        connection = sqlite3.connect("habit_tracker.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO habits (name, frequency) VALUES (?, ?)", (self.name, self.frequency))
        connection.commit()
        connection.close()

    def complete(self):
        # Mark habit as completed and log it
        connection = sqlite3.connect("habit_tracker.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM habits WHERE name=?", (self.name,))
        habit_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO habit_logs (habit_id, date, completed) VALUES (?, ?, ?)",
                       (habit_id, datetime.date.today(), 1))
        connection.commit()
        connection.close()

    def update_analytics(self):
        # Update analytics in the database
        connection = sqlite3.connect("habit_tracker.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM habits WHERE name=?", (self.name,))
        habit_data = cursor.fetchone()
        if habit_data:
            habit_id = habit_data[0]
            cursor.execute("SELECT * FROM habit_logs WHERE habit_id=?", (habit_id,))
            logs = cursor.fetchall()
            self.longest_streak = self.calculate_longest_streak(logs)
            self.current_streak = self.calculate_current_streak(logs)
            self.completion_rate = self.calculate_completion_rate(logs)
            cursor.execute("UPDATE habits SET longest_streak=?, current_streak=?, completion_rate=? WHERE id=?",
                           (self.longest_streak, self.current_streak, self.completion_rate, habit_id))
            connection.commit()
        connection.close()

    def calculate_longest_streak(self, logs):
        # Calculate longest streak
        longest_streak = 0
        current_streak = 0
        for log in logs:
            if log[3] == 1:
                current_streak += 1
            else:
                longest_streak = max(longest_streak, current_streak)
                current_streak = 0
        return max(longest_streak, current_streak)

    def calculate_current_streak(self, logs):
        # Calculate current streak
        current_streak = 0
        for log in logs:
            if log[3] == 1:
                current_streak += 1
            else:
                break
        return current_streak

    def calculate_completion_rate(self, logs):
        # Calculate completion rate
        total_logs = len(logs)
        if total_logs == 0:
            return 0
        completed_logs = sum(log[3] for log in logs)
        return round((completed_logs / total_logs) * 100, 2)
