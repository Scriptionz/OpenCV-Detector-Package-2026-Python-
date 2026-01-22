# 📜 Version History - OpenCV Detector

All major updates and technical improvements for the OpenCV object recognition engine are documented below.

## [1.3.3] - 2026-01-20
### Added
- **Scientific Precision:** Integrated the circularity formula $4\pi \times \frac{\text{Area}}{\text{Perimeter}^2}$ for 100% precision in circle identification.
- **Live Telemetry:** Added a real-time HUD for **FPS** and **Latency** monitoring to track hardware performance.

### Fixed
- **UI Stabilization:** Resolved frame timing conflicts and fixed text overlap issues on high-resolution displays.

## [1.3.2] - 2026-01-08
### Added
- **Target Tracking:** Implemented **LOCKED** bounding boxes for improved visual persistence on moving objects.
- **Lighting Auto-Correction:** Added **Histogram Equalization** to stabilize detection under shifting light conditions.

### Improved
- **Noise Reduction:** Optimized **Gaussian Blur** and **Morphological "Closing"** filters to eliminate sensor flicker.

## [1.3.1] - 2026-01-05
### Improved
- **Optimization:** Significant memory footprint reduction for sustained real-time video processing.

### Fixed
- **Logic Fix:** Corrected shape classification errors caused by high-frequency pixel noise (vertex count vs. ghosting).

## [1.2.0] - 2025-12-28
### Added
- **Geometric Expansion:** Full support for **Triangle**, **Rectangle**, and **Polygon** detection.
- **Architectural Split:** Introduced the `DETECTION_PARAMS` dictionary for "tuning without touching" the core logic.

## [1.1.0] - 2025-11-13
### Added
- **Interface Modularization:** Added dynamic UI overlays including status bars and crosshair indicators.

### Improved
- **Environmental Tuning:** Calibrated HSV sensitivity for better performance in variable outdoor environments.

## [1.0.0] - 2025-11-02
### Added
- **Core Engine:** Initial release of the primary Color Detection engine.
- **Point Analysis:** Implemented center-point pixel color analyzer (Crosshair Logic).
- **Stream Handling:** High-speed camera acquisition logic established.

---
**Developed by [Emir Karadağ](https://github.com/Scriptionz) © 2026**
