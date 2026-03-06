# Jime Robot Controller

This repository contains the dual-processor control system for the Jime Robot, integrating high-level vision and logic on a **Raspberry Pi** with low-level safety and motor control on an **ESP32**.

---

### System Architecture

The system operates using a distributed "Brain" and "Muscle" model:

* **Raspberry Pi (The Brain)**: Runs ROS 2 (Humble) to process YOLOv8 person detection, MediaPipe gesture recognition, and the master state machine.
* **ESP32 (The Muscle)**: Handles real-time hardware tasks, including PWM motor signals and autonomous obstacle avoidance via a triple-ultrasound sensor array.

---

## Project Structure

```text
ros2_ws/
├── yolov8n.pt               # Pre-trained YOLOv8 weights
└── src/
    └── jime_controller/
        ├── launch/
        │   └── jime_launch.py       # Launches all nodes simultaneously
        ├── jime_controller/
        │   ├── jime_brain.py        # Master State Machine
        │   ├── yolo_detector.py     # YOLOv8 Vision node
        │   ├── gesture_detector.py  # MediaPipe Gesture node
        │   └── serial_bridge.py     # Pi-to-ESP32 Communication
        └── esp32_firmware/
            └── motor_safety.ino     # ESP32 code for PWM and obstacle avoidance

```


---

## Safety Features

* **Hardware Override**: The ESP32 will cut PWM power to motors instantly if an obstacle is detected, even if the Pi is still sending movement commands.
* **Status Feedback**: The ESP32 sends `OBSTACLE_LEFT`, `OBSTACLE_CENTER`, or `OBSTACLE_RIGHT` via serial to inform the Pi for smart recovery.
