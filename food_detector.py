# food_detector.py
#
# VERSION 1
#
# from ultralytics import YOLO
# import cv2
#
# # === Load YOLOv8 model ===
# model = YOLO("yolov8n.pt")  # Automatically downloads if not found
#
# # === Full COCO class names ===
# class_names = [
#     "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
#     "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog",
#     "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
#     "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
#     "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
#     "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
#     "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor",
#     "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
#     "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
# ]
#
# # === Only allow food classes ===
# FOOD_CLASSES = {
#     "banana", "apple", "sandwich", "orange", "broccoli", "carrot",
#     "hot dog", "pizza", "donut", "cake"
# }
#
#
# def detect_food_from_webcam(conf_threshold=0.5):
#     """
#     Detect only food items using YOLOv8 from webcam feed
#     """
#     cap = cv2.VideoCapture(0)
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         results = model(frame)[0]
#
#         for result in results.boxes.data.tolist():
#             x1, y1, x2, y2, score, class_id = result
#             if score < conf_threshold:
#                 continue
#
#             class_id = int(class_id)
#             label = class_names[class_id] if class_id < len(class_names) else f"id:{class_id}"
#
#             # Filter only food items
#             if label.lower() not in FOOD_CLASSES:
#                 continue
#
#             # Draw bounding box and label
#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
#             cv2.putText(frame, f"{label} {score:.2f}", (int(x1), int(y1) - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
#
#         cv2.imshow("🍱 Smart Diet Tracker - Food Detection", frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()

# -----------------------------------------------------------------------------------------------------------

# VERSION 2

# food_detector.py

from ultralytics import YOLO
import cv2
from calorie_database import calorie_data

# === Load YOLOv8 model ===
model = YOLO("yolov8n.pt")

# === COCO class names ===
class_names = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog",
    "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
    "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
    "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor",
    "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

# Only allow food classes that exist in calorie database
FOOD_CLASSES = set(calorie_data.keys())

def detect_food_from_webcam(conf_threshold=0.5):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]

        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score < conf_threshold:
                continue

            class_id = int(class_id)
            label = class_names[class_id].lower()

            # Skip if not in our calorie database
            if label not in FOOD_CLASSES:
                continue

            calories = calorie_data[label]
            display_text = f"{label.title()} | {calories} kcal"

            # Draw bounding box and text
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, display_text, (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("🍱 Smart Diet Tracker - Food Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
