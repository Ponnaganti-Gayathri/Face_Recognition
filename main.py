import cv2
import pickle
import face_recognition
import numpy as np
import cvzone
import sqlite3
from datetime import datetime
from ultralytics import YOLO
import time
import os

# ======================
# ⚙️ Helper: Database Setup
# ======================
def init_db():
    conn = sqlite3.connect('emp_logs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empid TEXT,
            entry_time TEXT,
            exit_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_entry(empid):
    conn = sqlite3.connect('emp_logs.db')
    c = conn.cursor()
    entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO logs (empid, entry_time, exit_time) VALUES (?, ?, ?)", (empid, entry_time, None))
    conn.commit()
    conn.close()
    print(f"🟢 Entry logged for {empid} at {entry_time}")

def log_exit(empid):
    conn = sqlite3.connect('emp_logs.db')
    c = conn.cursor()
    exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("UPDATE logs SET exit_time = ? WHERE empid = ? AND exit_time IS NULL", (exit_time, empid))
    conn.commit()
    conn.close()
    print(f"🔴 Exit logged for {empid} at {exit_time}")

# Initialize DB
init_db()

# ======================
# ⚙️ Load YOLO and Encodings
# ======================
model = YOLO('yolov8n.pt')

if not os.path.exists('encodefile.p'):
    print("❌ encodefile.p not found! Run encodegenerator.py first.")
    exit()

with open('encodefile.p', 'rb') as file:
    encodelistknownWithIds = pickle.load(file)

encodeListKnown, empIds = encodelistknownWithIds
print(f"✅ Loaded encodings for {len(empIds)} employees")

# ======================
# ⚙️ Camera Setup
# ======================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Could not access webcam.")
    exit()

current_emps = set()
frame_skip = 2
frame_count = 0

# ======================
# 🎥 Main Loop
# ======================
while True:
    success, img = cap.read()
    if not success:
        print("⚠️ Frame capture failed.")
        break

    frame_count += 1
    if frame_count % frame_skip != 0:
        continue

    start_time = time.time()
    img_resized = cv2.resize(img, (960, 720))  # higher resolution for better detection

    # YOLO face detection
    results = model(img_resized, classes=[0])
    detected_emps = set()

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            face_img = img_resized[y1:y2, x1:x2]

            if face_img.size == 0:
                continue

            face_img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(face_img_rgb)

            if encodings:
                encodeFace = encodings[0]
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex] and faceDis[matchIndex] < 0.45:
                    empid = empIds[matchIndex]
                else:
                    empid = "Unknown"

                detected_emps.add(empid)
                color = (0, 255, 0) if empid != "Unknown" else (0, 0, 255)
                cvzone.cornerRect(img_resized, (x1, y1, x2 - x1, y2 - y1), rt=2, colorC=color)
                cv2.putText(img_resized, empid, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Log entry and exit
    new_entries = detected_emps - current_emps
    exited_emps = current_emps - detected_emps

    for emp in new_entries:
        if emp != "Unknown":
            log_entry(emp)

    for emp in exited_emps:
        if emp != "Unknown":
            log_exit(emp)

    current_emps = detected_emps

    fps = 1 / (time.time() - start_time)
    cv2.putText(img_resized, f'FPS: {int(fps)}', (15, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # 🖥️ Display Window
    cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Face Recognition", 960, 720)  # Default medium size
    cv2.imshow("Face Recognition", img_resized)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('f'):  # Toggle fullscreen
        cv2.setWindowProperty("Face Recognition", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    elif key == ord('n'):  # Normal window
        cv2.setWindowProperty("Face Recognition", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
    elif key == ord('q'):  # Quit
        break

cap.release()
cv2.destroyAllWindows()
print("🛑 Program closed.")
