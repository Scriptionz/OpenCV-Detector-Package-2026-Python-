# 🏛️ System Architecture - OpenCV Detector

This document outlines the core logic and processing pipeline of the **OpenCV Detector 2026**. The architecture is designed for high-precision object recognition with a focus on modularity and environmental adaptation.

---

### 1. Dependency Management
The system features a **self-healing dependency check**. 
* **Auto-Verification:** It verifies `OpenCV` and `NumPy` on startup.
* **Auto-Recovery:** If libraries are missing, the system auto-installs them via subprocess and restarts to maintain environment integrity.

### 2. Modular Configuration Layer
Global parameters (UI labels, feature toggles, camera specs) are decoupled into modular dictionaries. 
* This architecture enables **"tuning without touching"** the core computer vision algorithms.
* Facilitates rapid prototyping and easy customization for different hardware setups.

### 3. Vision & Processing Pipeline
The detection engine follows a strictly ordered pipeline:
1. **Acquisition:** High-speed real-time frame capture from `CAM_CONFIG` index.
2. **Pre-Processing:** Converts to HSV color space and applies adaptive **Gaussian Blurring** to eliminate digital flicker and sensor jitter.
3. **Lighting Stabilization:** Uses **Histogram Equalization** to maintain detection accuracy under variable outdoor lighting conditions.
4. **Morphological Refinement:** Executes `OPEN/CLOSE` operations to eliminate pixel gaps and "ghosting" artifacts in low-quality streams.

### 4. Scientific Object Recognition
Advanced mathematical logic is used for precise shape identification:
* **Contour Analysis:** Extracts structural outlines and filters by `min_area`.
* **Polygon Approximation:** Implements the **Douglas-Peucker algorithm** for vertex mapping.
* **Circularity Analysis:** Uses the mathematical roundness formula:  
  $$4 \pi \times \frac{\text{Area}}{\text{Perimeter}^2}$$  
  to verify circles regardless of pixel distortion.
* **Target Tracking:** Dynamic Bounding Box logic (LOCKED) for real-time visual identification.

### 5. Telemetry & UI
The system renders a real-time **HUD (Heads-Up Display)** which includes:
* Shape and Color labels.
* Performance telemetry (FPS and Latency tracking).
* Integrated crosshair color analysis.

---

> [!CAUTION]
> **Termination:** To shut down the application, press the key defined in `CAM_CONFIG` (Default: **"q"**). Closing the window manually or forcing a kill may lead to resource leaks (camera handle issues).
