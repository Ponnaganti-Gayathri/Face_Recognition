# Real-Time Face Recognition & Attendance System

This project implements a real-time face recognition system for logging employee entries and exits. It uses **YOLOv8** for face detection, **Face Recognition** library for encoding and matching faces, and **SQLite** to maintain attendance logs. Unknown faces can be optionally saved for future recognition.
---

## Features

- Real-time face detection using YOLOv8.
- Face encoding and recognition for known employees.
- Automatic logging of entry and exit times in SQLite database.
- Supports adding new faces via popup for unknown individuals.
- Toggle between normal and fullscreen display while monitoring.
- Adjustable detection threshold and frame skipping for performance.

---

## Installation

Clone the repository:
git clone <your-repo-url>
cd face_recognition-main

Create and activate a virtual environment:
python -m venv venv
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Download YOLOv8 model:
Download yolov8n.pt and place it in the project root.

Add employee images:
Create an images folder and add employee face images. Use the employee name or ID as the image filename.

Usage:

Generate face encodings:
python encodegenerator.py

Run the main program:
python main.py

Controls:
Press f to toggle fullscreen.
Press n to return to normal window.
Press q to quit.

Folder Structure:

face_recognition-main/

images/ (Employee face images)

encodegenerator.py (Script to encode faces)

main.py (Main face recognition script)

encodefile.p (Encoded face data, generated)

yolov8n.pt (YOLOv8 face detection model)

emp_logs.db (SQLite database for logs)

requirements.txt (Python dependencies)

Dependencies:
Python 3.9+
OpenCV (cv2)
face_recognition
cvzone
numpy
ultralytics (YOLOv8)
SQLite3 (built-in)

License:
This project is licensed under the MIT License. See LICENSE for details.

Acknowledgements:
YOLOv8 for real-time object detection.
face_recognition for face encoding and matching_
