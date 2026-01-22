# 📜 Version History - OpenCV Detector

All major updates and technical improvements for the OpenCV object recognition engine are documented below.

---

### 🚀 [v1.3.3] - 2026-01-20 | **LATEST**
> **"Scientific Precision Update"**

* **Mathematical Accuracy:** Integrated the circularity formula $4\pi \times \frac{\text{Area}}{\text{Perimeter}^2}$ for 100% precision in circle identification.
* **Live Telemetry:** Added a real-time HUD for **FPS** and **Latency** monitoring to track hardware performance.
* **UI Stabilization:** Resolved frame timing conflicts and fixed text overlap issues on high-resolution displays.

---

### 🛠️ [v1.3.2] - 2026-01-08
> **"Visual Stability & Lighting Enhancement"**

* **Noise Reduction:** Optimized **Gaussian Blur** and **Morphological "Closing"** filters to eliminate sensor flicker.
* **Target Tracking:** Implemented **LOCKED** bounding boxes for improved visual persistence on moving objects.
* **Lighting Auto-Correction:** Added **Histogram Equalization** to stabilize detection under shifting light conditions.

---

### 🔍 [v1.3.1] - 2026-01-05
* **Logic Fix:** Corrected shape classification errors caused by high-frequency pixel noise.
* **Optimization:** Significant memory footprint reduction for sustained real-time video processing.

---

### 📐 [v1.2.0] - 2025-12-28
* **Geometric Expansion:** Full support for **Triangle**, **Rectangle**, and **Polygon** detection.
* **Architectural Split:** Introduced the `DETECTION_PARAMS` dictionary, allowing core logic tuning without code modification.

---

### 🎨 [v1.1.0] - 2025-11-13
* **Interface Modularization:** Added dynamic UI overlays including status bars and crosshair indicators.
* **Environmental Tuning:** Calibrated HSV sensitivity for better performance in variable outdoor environments.

---

### ✨ [v1.0.0] - 2025-11-02 | **INITIAL**
* **Core Engine:** Launched the primary Color Detection system.
* **Point Analysis:** Implemented center-point pixel color analyzer.
* **Stream Handling:** High-speed camera acquisition logic established.

---
**Developed by [Emir Karadağ](https://github.com/Scriptionz) © 2026**
