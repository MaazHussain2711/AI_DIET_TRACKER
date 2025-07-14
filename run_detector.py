# run_detector.py

from food_detector import detect_food_from_webcam

if __name__ == "__main__":
    detect_food_from_webcam(conf_threshold=0.4)
