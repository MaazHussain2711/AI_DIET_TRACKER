# 🥗 Smart Diet Tracker | AI_Diet_Tracker

A smart AI-powered food recognition and calorie tracking system using **YOLOv8**, **PyQt5**, and **Python**.

---

## ⚙️ Features

- 👤 User profile setup (Name, Age, Weight, Height, Goal)
- 📸 Capture food via webcam
- 🧠 Real-time food detection with YOLOv8
- 🔥 Calorie estimation via built-in food DB
- 📊 Daily log tracking with PyQt5 dashboard
- 📈 Donut chart showing calorie goal vs intake

---

## 🛠️ Tech Stack

| Component       | Library           |
|----------------|-------------------|
| Detection       | YOLOv8 (`ultralytics`) |
| UI              | PyQt5             |
| Plotting        | Matplotlib        |
| Image Capture   | OpenCV            |

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8 or above

### 📦 Install dependencies

pip install -r requirements.txt
💻 Run the app
python ui_main.py
📂 Project Structure
AI_DIET_TRACKER/
│
├── user_profile.py         # BMR, TDEE, goal calc
├── calorie_database.py     # Food:Calorie data
├── food_detector.py        # YOLOv8 detection core
├── tracker.py              # Handles detection, logging
├── ui_main.py              # PyQt5 GUI entry point
├── tracker_log.json        # Food tracking logs
├── requirements.txt
├── README.md
└── assets/
    └── captured_food.jpg   # Webcam snapshot placeholder
🤖 AI Used
Pretrained YOLOv8 model (Ultralytics) for real-time object detection

Custom food filter for calorie mapping

🧠 Future Add-ons
 Weekly trend plots 📈

 Portion size estimation from image 📏

 Food recommendation using ML 🔁

 Streamlit web deployment 🌐

👤 Author
Made by Maaz Hussain
