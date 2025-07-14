# ui_main.py

import sys
import json
import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from user_profile import UserProfile
from calorie_database import calorie_data
from tracker import capture_food_photo, detect_food, log_food_entry, load_existing_user

class SmartDietTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Diet Tracker 🍽️")
        self.setGeometry(200, 100, 800, 600)
        self.init_ui()

        self.username = ""
        self.profile = {}
        self.goal = 0
        self.total_today = 0

    def init_ui(self):
        layout = QVBoxLayout()

        # User Info Section
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setFont(QFont("Arial", 12))

        self.load_button = QPushButton("Load Profile")
        self.load_button.clicked.connect(self.load_profile)

        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("👤 Name: "))
        name_row.addWidget(self.name_input)
        name_row.addWidget(self.load_button)
        layout.addLayout(name_row)

        # Capture Food
        self.capture_button = QPushButton("📸 Capture Food & Detect")
        self.capture_button.setEnabled(False)
        self.capture_button.clicked.connect(self.capture_and_detect)
        layout.addWidget(self.capture_button)

        # Food Output
        self.output_label = QLabel("")
        self.output_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.output_label)

        # Plot area
        self.figure = Figure(figsize=(3, 3))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Table of today's log
        self.table = QTableWidget()
        layout.addWidget(QLabel("📅 Today's Food Log"))
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_profile(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter your name.")
            return

        self.username = name
        profile = load_existing_user(name)

        if profile:
            self.profile = profile
            self.goal = round(UserProfile(
                name, profile["age"], profile["gender"], profile["height"],
                profile["weight"], "moderate", profile["goal"]
            ).get_calorie_goal())
            QMessageBox.information(self, "Profile Loaded", f"Welcome back, {name}!\nCalorie Goal: {self.goal} kcal")
            self.capture_button.setEnabled(True)
            self.update_today_table()
            self.update_plot()
        else:
            QMessageBox.warning(self, "Profile Missing", "No profile found. Please run tracker.py first to set up.")

    def capture_and_detect(self):
        path = capture_food_photo("assets/captured_food.jpg")
        if not path:
            return

        food_items = detect_food(path)
        if not food_items:
            self.output_label.setText("⚠️ No food detected.")
            return

        total_cal = sum(calorie_data[item] for item in food_items)
        self.total_today += total_cal

        food_text = ", ".join(food_items)
        self.output_label.setText(f"🍕 Detected: {food_text} | 🔥 {total_cal} kcal")

        # Log it
        log_food_entry(self.username, food_items, total_cal, self.goal, self.profile)

        # Update UI
        self.update_today_table()
        self.update_plot()

    def update_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        eaten = self.get_today_total()
        remaining = max(0, self.goal - eaten)

        ax.pie([eaten, remaining], labels=["Eaten", "Remaining"],
               autopct="%1.1f%%", colors=["#ff9999", "#99ff99"])
        ax.set_title("Calorie Progress")
        self.canvas.draw()

    def update_today_table(self):
        try:
            with open("tracker_log.json", "r") as f:
                logs = json.load(f)
        except:
            logs = []

        today = datetime.date.today().isoformat()
        filtered = [entry for entry in logs if entry["user"] == self.username and entry["timestamp"].startswith(today)]

        self.table.setRowCount(len(filtered))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Time", "Foods", "Calories"])

        for i, entry in enumerate(filtered):
            self.table.setItem(i, 0, QTableWidgetItem(entry["timestamp"].split()[1]))
            self.table.setItem(i, 1, QTableWidgetItem(", ".join(entry["foods"])))
            self.table.setItem(i, 2, QTableWidgetItem(str(entry["total_calories"])))

    def get_today_total(self):
        try:
            with open("tracker_log.json", "r") as f:
                logs = json.load(f)
        except:
            logs = []

        today = datetime.date.today().isoformat()
        total = sum(entry["total_calories"]
                    for entry in logs if entry["user"] == self.username and entry["timestamp"].startswith(today))
        return total

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartDietTracker()
    window.show()
    sys.exit(app.exec_())
