# Scripted by @Emir Karadağ v14.7 [2025-2026]
# GitHub: @Scriptionz [https://github.com/Scriptionz] 
# LinkedIn: @Emir Karadağ [https://www.linkedin.com/in/emir-karadağ-617a013a2/]

# !! Licensed under the MIT License. Please check the license before using the system. !!

# --------------- LIBRARY IMPORTER (AUTO) ----------------- #
import os
import sys
import subprocess
import time

def install_dependencies():
    """Checks for required libraries and installs them if missing."""
    required = {'opencv-python', 'numpy'}
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("SYSTEM: Missing libraries detected. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *required])
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            print(f"FATAL ERROR 003: {e}")
            sys.exit()

install_dependencies()

import cv2
import numpy as np

# --------------- CONFIGURATION & LOCALIZATION ----------------- #

CURRENT_VERSION = "v1.3.3"
LANGUAGE_SETTINGS = {
    "startup_msg": f"UAV X DEVELOPMENT - {CURRENT_VERSION} Loading...",
    "err_no_cam": "ERROR 001: Camera not detected.",
    "err_frame_lost": "ERROR 032: Frame lost.",
    "ui_window_name": f"UAV Vision System - {CURRENT_VERSION}",
    "color_names": {
        "red": "RED", "orange": "ORANGE", "yellow": "YELLOW",
        "green": "GREEN", "blue": "BLUE", "purple": "PURPLE"
    },
    "shape_labels": {
        "tri": "TRIANGLE", "rect": "RECTANGLE", "pent": "PENTAGON",
        "hex": "HEXAGON", "poly": "POLYGON", "circle": "CIRCLE"
    }
}

SETTINGS = {
    "dot_color_reader": True,       # Analyzes the color of the center pixel
    "shape_detection": False,        # Detects geometric patterns
    "telemetry_overlay": True,      # Displays FPS and Latency
    "auto_brightness": True,        # Histogram Equalization for light stability
    "target_identifier": True       # Visual 'LOCKED' box for targets
}

DETECTION_PARAMS = {
    "min_area": 4500,               # Minimum area to filter out noise
    "blur_size": (15, 15),          # Gaussian blur to prevent flickering
    "epsilon_coeff": 0.04,          # Polygon approximation tolerance
    "line_thickness": 2,            # UI drawing thickness
    "hsv_lower": np.array([0, 70, 50]),
    "hsv_upper": np.array([180, 255, 255]),
    "circularity_threshold": 0.75   # Threshold for mathematical circle verification
}

CAM_CONFIG = {
    "width": 1280, "height": 720,
    "device_index": 0, "exit_key": "q"
}

# --------------- CORE SYSTEM ----------------- #

print(LANGUAGE_SETTINGS["startup_msg"])
cap = cv2.VideoCapture(CAM_CONFIG["device_index"])
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_CONFIG["width"])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_CONFIG["height"])

if not cap.isOpened():
    print(LANGUAGE_SETTINGS["err_no_cam"])
    sys.exit()

prev_time = time.time() 

while True:
    ret, frame = cap.read()
    if not ret: break

    # --- [STEP 1: LIGHTING STABILIZATION] --- 
    # Balances exposure for outdoor flight stability
    if SETTINGS["auto_brightness"]:
        img_yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        frame = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    # --- [STEP 2: COLOR ANALYSIS] ---
    # Identifies the color at the center crosshair using HSV space
    if SETTINGS["dot_color_reader"]:
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape
        cx, cy = width // 2, height // 2
        hue = hsv_frame[cy, cx][0]
        b, g, r = map(int, frame[cy, cx])

        c = LANGUAGE_SETTINGS["color_names"]
        if hue < 5 or hue > 170: color_str = c["red"]
        elif hue < 22: color_str = c["orange"]
        elif hue < 33: color_str = c["yellow"]
        elif hue < 78: color_str = c["green"]
        elif hue < 131: color_str = c["blue"]
        else: color_str = c["purple"]

        # Render UI crosshair and color status
        cv2.rectangle(frame, (cx - 150, 600), (cx + 150, 680), (255, 255, 255), -1)
        cv2.putText(frame, color_str, (cx - 100, 655), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (b, g, r), 3)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), 2)

    # --- [STEP 3: SHAPE DETECTION] ---
    # Masks image, removes paratistics, and classifies geometric forms
    if SETTINGS["shape_detection"]:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
        blurred_hsv = cv2.GaussianBlur(hsv, DETECTION_PARAMS["blur_size"], 0) 
        mask = cv2.inRange(blurred_hsv, DETECTION_PARAMS["hsv_lower"], DETECTION_PARAMS["hsv_upper"])

        # Morphological Operations: Closes small holes and removes noise
        kernel = np.ones((7,7), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Detect stable contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > DETECTION_PARAMS["min_area"]:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, DETECTION_PARAMS["epsilon_coeff"] * peri, True)
                
                # Mathematical Circularity Formula (4*PI*Area / Peri^2)
                # Measures 'roundness' regardless of corner counts
                circularity = (4 * np.pi * area) / (peri**2)
                
                label = "UNKNOWN"
                if circularity > DETECTION_PARAMS["circularity_threshold"]:
                    label = LANGUAGE_SETTINGS["shape_labels"]["circle"]
                elif len(approx) == 3: label = LANGUAGE_SETTINGS["shape_labels"]["tri"]
                elif len(approx) == 4: label = LANGUAGE_SETTINGS["shape_labels"]["rect"]
                elif 5 <= len(approx) <= 6: label = LANGUAGE_SETTINGS["shape_labels"]["poly"]
                else: continue

                # Target Tracking Visuals (Bounding Box)
                x, y, w, h = cv2.boundingRect(approx)
                if SETTINGS["target_identifier"]:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 1)
                    cv2.putText(frame, "LOCKED", (x, y+h+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

                cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # --- [STEP 4: TELEMETRY & PERFORMANCE] ---
    # Measures system FPS and processing latency
    if SETTINGS["telemetry_overlay"]:
        now = time.time()
        fps = 1 / (now - prev_time) if (now - prev_time) > 0 else 0
        prev_time = now
        cv2.putText(frame, f"FPS: {int(fps)} | LATENCY: {int((1/fps)*1000) if fps>0 else 0}ms", 
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow(LANGUAGE_SETTINGS["ui_window_name"], frame)
    if cv2.waitKey(1) & 0xFF == ord(CAM_CONFIG["exit_key"]): break

cap.release()
cv2.destroyAllWindows()
