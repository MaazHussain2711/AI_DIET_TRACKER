# VERSION 1

# # tracker.py
#
# import cv2
# import json
# import datetime
# from user_profile import UserProfile
# from calorie_database import calorie_data
# from ultralytics import YOLO
#
# # === Load YOLOv8 model
# model = YOLO("yolov8n.pt")
#
# # === Allowed food items
# FOOD_CLASSES = set(calorie_data.keys())
#
# # === Capture photo from webcam
# def capture_food_photo(filename="captured_food.jpg"):
#     cam = cv2.VideoCapture(0)
#     print("📸 Press SPACE to capture image, ESC to exit")
#
#     while True:
#         ret, frame = cam.read()
#         if not ret:
#             break
#
#         cv2.imshow("Capture Food Image", frame)
#         key = cv2.waitKey(1)
#         if key % 256 == 27:  # ESC
#             print("❌ Capture cancelled.")
#             cam.release()
#             cv2.destroyAllWindows()
#             return None
#         elif key % 256 == 32:  # SPACE
#             cv2.imwrite(filename, frame)
#             print(f"✅ Image saved as {filename}")
#             cam.release()
#             cv2.destroyAllWindows()
#             return filename
#
# # === Detect food in image
# def detect_food(image_path):
#     image = cv2.imread(image_path)
#     results = model(image)[0]
#     detected = []
#
#     for result in results.boxes.data.tolist():
#         x1, y1, x2, y2, score, class_id = result
#         label = model.names[int(class_id)].lower()
#         if label in FOOD_CLASSES:
#             detected.append(label)
#
#     return detected
#
# # === Log entry to file
# def log_food_entry(name, food_list, total_calories, calorie_goal):
#     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     entry = {
#         "timestamp": now,
#         "user": name,
#         "foods": food_list,
#         "total_calories": total_calories,
#         "daily_goal": calorie_goal
#     }
#
#     try:
#         with open("tracker_log.json", "r") as f:
#             data = json.load(f)
#     except FileNotFoundError:
#         data = []
#
#     data.append(entry)
#
#     with open("tracker_log.json", "w") as f:
#         json.dump(data, f, indent=4)
#
#     print("📦 Entry logged successfully!\n")
#
# # === Main logic
# def run_tracker():
#     print("👤 Enter your details:")
#     name = input("Name: ")
#     age = int(input("Age: "))
#     gender = input("Gender (Male/Female): ")
#     height = float(input("Height (cm): "))
#     weight = float(input("Weight (kg): "))
#
#     print("\n🎯 Your goal:")
#     print("1. Lose Weight")
#     print("2. Maintain Weight")
#     print("3. Gain Weight")
#     goal_map = {"1": "lose", "2": "maintain", "3": "gain"}
#     goal_input = input("Choose (1-3): ")
#     goal = goal_map.get(goal_input, "maintain")
#
#     # === Create user profile
#     user = UserProfile(name, age, gender, height, weight, "moderate", goal)
#     daily_goal = user.get_calorie_goal()
#
#     print(f"\n🔍 Daily Calorie Target: {round(daily_goal)} kcal")
#
#     # === Capture and detect
#     img_path = capture_food_photo()
#     if not img_path:
#         return
#
#     food_items = detect_food(img_path)
#     if not food_items:
#         print("⚠️ No food items detected.")
#         return
#
#     # === Calculate calories
#     total_calories = sum(calorie_data[item] for item in food_items)
#     print(f"\n🍽️ You are about to eat: {', '.join(food_items)}")
#     print(f"🔥 Total Calories: {total_calories} kcal")
#
#     # === Impact analysis
#     remaining = daily_goal - total_calories
#     if remaining > 0:
#         print(f"✅ You're within your goal. Remaining: {round(remaining)} kcal")
#     else:
#         print(f"⚠️ You've exceeded your goal by {abs(round(remaining))} kcal")
#
#     # === Log it
#     log_food_entry(name, food_items, total_calories, round(daily_goal))
#
# # === Run main tracker
# if __name__ == "__main__":
#     run_tracker()

# --------------------------------------------------------------------------------------------------------------
# tracker.py

import cv2
import json
import datetime
from user_profile import UserProfile
from calorie_database import calorie_data
from ultralytics import YOLO

# === Load YOLOv8 model
model = YOLO("yolov8n.pt")

# === Allowed food items
FOOD_CLASSES = set(calorie_data.keys())


def capture_food_photo(filename="captured_food.jpg"):
    cam = cv2.VideoCapture(0)
    print("📸 Press SPACE to capture image, ESC to exit")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        cv2.imshow("Capture Food Image", frame)
        key = cv2.waitKey(1)
        if key % 256 == 27:  # ESC
            print("❌ Capture cancelled.")
            cam.release()
            cv2.destroyAllWindows()
            return None
        elif key % 256 == 32:  # SPACE
            cv2.imwrite(filename, frame)
            print(f"✅ Image saved as {filename}")
            cam.release()
            cv2.destroyAllWindows()
            return filename


def detect_food(image_path):
    image = cv2.imread(image_path)
    results = model(image)[0]
    detected = []

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        label = model.names[int(class_id)].lower()
        if label in FOOD_CLASSES:
            detected.append(label)

    return detected


def load_existing_user(name):
    try:
        with open("tracker_log.json", "r") as f:
            logs = json.load(f)
        for entry in reversed(logs):  # Check latest first
            if entry["user"] == name and "profile" in entry:
                return entry["profile"]
    except FileNotFoundError:
        return None
    return None


def log_food_entry(name, food_list, total_calories, calorie_goal, profile):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": now,
        "user": name,
        "profile": profile,
        "foods": food_list,
        "total_calories": total_calories,
        "daily_goal": calorie_goal
    }

    try:
        with open("tracker_log.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(entry)

    with open("tracker_log.json", "w") as f:
        json.dump(data, f, indent=4)

    print("📦 Entry logged successfully!\n")


def run_tracker():
    print("👤 Enter your name:")
    name = input("Name: ")

    existing_profile = load_existing_user(name)

    if existing_profile:
        print(f"✅ Found saved profile for {name}")
        age = existing_profile["age"]
        gender = existing_profile["gender"]
        height = existing_profile["height"]
        weight = existing_profile["weight"]
        goal = existing_profile["goal"]
    else:
        print("🔁 No existing profile found. Please enter details:")
        age = int(input("Age: "))
        gender = input("Gender (Male/Female): ")
        height = float(input("Height (cm): "))
        weight = float(input("Weight (kg): "))

        print("\n🎯 Your goal:")
        print("1. Lose Weight")
        print("2. Maintain Weight")
        print("3. Gain Weight")
        goal_map = {"1": "lose", "2": "maintain", "3": "gain"}
        goal_input = input("Choose (1-3): ")
        goal = goal_map.get(goal_input, "maintain")

    # === Create UserProfile object
    user = UserProfile(name, age, gender, height, weight, "moderate", goal)
    daily_goal = round(user.get_calorie_goal())

    print(f"\n🔍 Daily Calorie Target: {daily_goal} kcal")

    # === Capture and detect
    img_path = capture_food_photo()
    if not img_path:
        return

    food_items = detect_food(img_path)
    if not food_items:
        print("⚠️ No food items detected.")
        return

    # === Calculate calories
    total_calories = sum(calorie_data[item] for item in food_items)
    print(f"\n🍽️ You are about to eat: {', '.join(food_items)}")
    print(f"🔥 Total Calories: {total_calories} kcal")

    # === Impact analysis
    remaining = daily_goal - total_calories
    if remaining > 0:
        print(f"✅ You're within your goal. Remaining: {round(remaining)} kcal")
    else:
        print(f"⚠️ You've exceeded your goal by {abs(round(remaining))} kcal")

    # === Log it
    profile_dict = {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "goal": goal
    }
    log_food_entry(name, food_items, total_calories, daily_goal, profile_dict)


if __name__ == "__main__":
    run_tracker()

