# Scripted by @Emir Karadağ v14.7 [2025-2026]
# GitHub: @Scriptionz [https://github.com/Scriptionz] 
# LinkedIn: @Emir Karadağ [https://www.linkedin.com/in/emir-karadağ-617a013a2/]

# # !! Licensed under the MIT License. !!

# --------------- VERSION HISTORY ----------------- #

# {LATEST} v1.3.2 - Final Modular Precision & Noise Filter - 8 January 2026
# {OLD} v1.3.1 - Fixed Shape Detection Logic - 8 January 2026
# {OLD} v1.3.0 - Modular Output Full - 8 January 2026
# {OLD} v1.2.0 - Shape Detection Update - 28 December 2025
# {OLD} v1.1.0 - Modular Output Beta - 13 November 2025
# {OLDEST} v1.0.0 - Color Detection - 2 November 2025

# Import Needed Libraries
import os
import sys
import subprocess

def install_dependencies(): # Checks libraries if its loaded or not
    """Checks and installs required libraries if they are missing."""
    required = {'opencv-python', 'numpy'}
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("SYSTEM: Missing libraries detected. Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *required])
            print("SYSTEM: Installation successful. Restarting script...")
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            print(f"FATAL ERROR 003: Could not install dependencies. {e}")
            sys.exit()

# Run Dependency Check
install_dependencies()

import cv2
import numpy as np

# --------------- CONFIGURATION & LOCALIZATION ----------------- #

# Output & Language Settings (Change your strings here)
LANGUAGE_SETTINGS = {
    "startup_msg": "UAV X DEVELOPMENT - System Loading...",
    "err_no_cam": "ERROR 001: Camera not detected. Please check connection.",
    "err_frame_lost": "ERROR 032: Failed to capture frame during operation.",
    "ui_window_name": "UAV Vision System - v1.3.2",
    "color_names": {
        "red": "RED",
        "orange": "ORANGE",
        "yellow": "YELLOW",
        "green": "GREEN",
        "blue": "BLUE",
        "purple": "PURPLE"
    },
    "shape_labels": {
        "tri": "TRIANGLE",
        "rect": "RECTANGLE",
        "pent": "PENTAGON",
        "hex": "HEXAGON",
        "poly": "POLYGON",
        "circle": "CIRCLE"
    }
}

# Feature Toggles (True/False)
SETTINGS = {
    "target_humanoids_WIP": False,
    "dot_color_reader": True,       # Focuses on the center point color
    "shape_detection": False,        # Detects geometric patterns
    "cam_color_reader_WIP": False,
    "target_identifier_WIP": True,
    "voice_feedback_WIP": False
}

# Fine-Tuning Detection Parameters (MODULAR TUNING)
DETECTION_PARAMS = {
    "min_area": 4500,               # Minimum object size (Increased to fix neck/ghost noise)
    "blur_size": (15, 15),          # High blur to fix pixel flickering
    "epsilon_coeff": 0.04,          # Tolerance (Higher = less sensitive to pixel jitters)
    "line_thickness": 2,            # Thickness of contours and circles
    "hsv_lower": np.array([0, 70, 50]),
    "hsv_upper": np.array([180, 255, 255]),
}

# Camera Settings
CAM_CONFIG = {
    "width": 1280,
    "height": 720,
    "device_index": 0,              # Which camera to run? [0 means 1st camera]
    "exit_key": "q"                 # Key to close the application
}

# --------------- CORE SYSTEM ----------------- #

print(LANGUAGE_SETTINGS["startup_msg"])

# Initialize Camera Stream
cap = cv2.VideoCapture(CAM_CONFIG["device_index"])
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_CONFIG["width"])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_CONFIG["height"])

if not cap.isOpened():
    print(LANGUAGE_SETTINGS["err_no_cam"])
    sys.exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print(LANGUAGE_SETTINGS["err_frame_lost"])
        break

    # --- Feature 1: Center Dot Color Reader ---
    if SETTINGS["dot_color_reader"]:
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape
        cx, cy = width // 2, height // 2

        # Analyze central pixel
        b, g, r = map(int, frame[cy, cx])
        hue = hsv_frame[cy, cx][0]

        # Logic for color classification
        colors = LANGUAGE_SETTINGS["color_names"]
        if hue < 5 or hue > 170: color_str = colors["red"]
        elif hue < 22: color_str = colors["orange"]
        elif hue < 33: color_str = colors["yellow"]
        elif hue < 78: color_str = colors["green"]
        elif hue < 131: color_str = colors["blue"]
        else: color_str = colors["purple"]

        # UI Overlay: Status Bar and Aiming Circle
        cv2.rectangle(frame, (cx - 150, 600), (cx + 150, 680), (255, 255, 255), -1)
        cv2.putText(frame, color_str, (cx - 100, 655), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (b, g, r), 3)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), DETECTION_PARAMS["line_thickness"])

    # --- Feature 2: Geometric Shape Detection ---
    if SETTINGS["shape_detection"]:
        # Pre-processing (Anti-Ghosting logic)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
        
        # Apply Modular Blur to handle low-quality camera flicker
        blurred_hsv = cv2.GaussianBlur(hsv, DETECTION_PARAMS["blur_size"], 0) 
        
        # Color Masking
        mask = cv2.inRange(blurred_hsv, DETECTION_PARAMS["hsv_lower"], DETECTION_PARAMS["hsv_upper"])

        # Morphological operations (Filling gaps and removing small pixel dots)
        kernel = np.ones((7,7), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Finding stable contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            
            # Area Filter: High threshold to ignore noisy neck/shoulder pixels
            if area > DETECTION_PARAMS["min_area"]:

                peri = cv2.arcLength(cnt, True)
                # Douglas-Peucker Polygon Approximation
                approx = cv2.approxPolyDP(cnt, DETECTION_PARAMS["epsilon_coeff"] * peri, True)
                
                corners = len(approx)
                x, y, w, h = cv2.boundingRect(approx)
                
                # Aspect Ratio Filter: Reject thin/weird shaped ghosts
                aspect_ratio = float(w)/h
                if 0.2 < aspect_ratio < 5.0:
                    labels = LANGUAGE_SETTINGS["shape_labels"]
                    
                    # Logic for Shape Classification
                    if corners == 3: label = labels["tri"]
                    elif corners == 4: label = labels["rect"]
                    elif 5 <= corners <= 6: label = labels["poly"]
                    elif corners > 7: label = labels["circle"]
                    else: continue

                    # Visual Rendering
                    cv2.drawContours(frame, [approx], 0, (0, 255, 0), DETECTION_PARAMS["line_thickness"])
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Render the Window
    cv2.imshow(LANGUAGE_SETTINGS["ui_window_name"], frame)

    # Close application using the custom key defined in CAM_CONFIG
    if cv2.waitKey(1) & 0xFF == ord(CAM_CONFIG["exit_key"]):
        break

# Clean exit process
cap.release()
cv2.destroyAllWindows()
