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

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd face_recognition-main
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Download the YOLOv8 model (yolov8n.pt) and place it in the project root.

Create an images folder and add employee face images (name of file = employee ID).

Usage
Generate face encodings:

bash
Copy code
python encodegenerator.py
Run the main program:

bash
Copy code
python main.py
Controls:

Press f to toggle fullscreen.

Press n to return to normal window.

Press q to quit.

Folder Structure
graphql
Copy code
face_recognition-main/
│
├─ images/               # Employee face images
├─ encodegenerator.py    # Script to encode faces
├─ main.py               # Main face recognition script
├─ encodefile.p          # Encoded face data (generated)
├─ yolov8n.pt            # YOLOv8 face detection model
├─ emp_logs.db           # SQLite database for logs
├─ requirements.txt      # Python dependencies
Dependencies
Python 3.9+

OpenCV (cv2)

face_recognition

cvzone

numpy

ultralytics (YOLOv8)

SQLite3 (built-in)

License
This project is licensed under the MIT License. See LICENSE for details.

Acknowledgements
YOLOv8 for real-time object detection.

face_recognition for face encoding and matching.

cvzone for bounding box visualization and UI enhancements.
