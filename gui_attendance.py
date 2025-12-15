import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import face_recognition
import numpy as np
import pandas as pd
import os
from datetime import datetime
import pyttsx3
from core import load_known_faces, recognize_faces_in_frame
import warnings
import threading
import time

# --- CONFIGURATION ---
warnings.filterwarnings("ignore")
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# --- VOICE FUNCTION ---
def speak(text):
    """Provide voice feedback safely."""
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        print(f"🔈 Voice failed for: {text}")

# --- ATTENDANCE LOGIC ---
def mark_attendance(name):
    """Mark attendance in CSV file with timestamp."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create CSV if missing or empty
    if not os.path.exists("attendance.csv") or os.stat("attendance.csv").st_size == 0:
        pd.DataFrame(columns=["Name", "Time"]).to_csv("attendance.csv", index=False)

    try:
        df = pd.read_csv("attendance.csv")
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=["Name", "Time"])

    # Prevent re-marking same person within same day
    today = datetime.now().strftime("%Y-%m-%d")
    df_today = df[df["Time"].str.startswith(today)] if not df.empty else pd.DataFrame()

    if name not in df_today["Name"].values:
        df.loc[len(df.index)] = [name, now]
        df.to_csv("attendance.csv", index=False)
        speak(f"Welcome {name}")
        print(f"✅ Marked attendance for {name}")
        update_status(f"✅ Marked: {name}")
    else:
        update_status(f"ℹ️ {name} already marked today")
        print(f"ℹ️ {name} already marked today")

# --- LOAD KNOWN FACES ---
try:
    encodeListKnown, studentNames = load_known_faces("Images")
    print("✅ Known faces loaded:", studentNames)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load known faces:\n{e}")
    raise SystemExit

# --- STATUS LABEL FUNCTION ---
def update_status(message):
    """Update the status label in GUI."""
    status_label.config(text=message)

# --- CLOCK FUNCTION ---
def update_clock():
    """Display real-time clock in GUI."""
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d %b %Y")
    clock_label.config(text=f"{current_date} | {current_time}")
    root.after(1000, update_clock)

# --- CAMERA MODE (Run in Thread) ---
def start_camera_mode():
    """Start webcam for real-time recognition."""
    threading.Thread(target=run_camera, daemon=True).start()

def run_camera():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Error", "Camera not found or already in use!")
        return

    speak("Starting live camera attendance system")
    update_status("🎥 Camera started — press 'q' to quit.")

    cv2.namedWindow("AttendX - Smart Attendance", cv2.WINDOW_NORMAL)
    while True:
        success, frame = cap.read()
        if not success:
            print("⚠️ Camera disconnected or not capturing.")
            update_status("⚠️ Camera disconnected.")
            break

        recognized_names = recognize_faces_in_frame(frame, encodeListKnown, studentNames)
        for name in recognized_names:
            mark_attendance(name)

        cv2.imshow("AttendX - Smart Attendance", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    speak("Attendance session ended")
    update_status("🧾 Camera closed successfully.")
    print("🧾 Camera closed successfully.")

# --- GROUP PHOTO MODE ---
def select_photo_mode():
    """Recognize faces from an uploaded group photo."""
    file_path = filedialog.askopenfilename(
        title="Select Group Photo",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if not file_path:
        return

    img = cv2.imread(file_path)
    if img is None:
        messagebox.showerror("Error", "Invalid image selected!")
        return

    recognized_names = recognize_faces_in_frame(img, encodeListKnown, studentNames)
    if recognized_names:
        for name in recognized_names:
            mark_attendance(name)
        messagebox.showinfo("Done", f"Attendance marked for: {', '.join(recognized_names)}")
        update_status(f"✅ Marked: {', '.join(recognized_names)}")
    else:
        messagebox.showwarning("No Match", "No known faces found in the image!")
        update_status("⚠️ No known faces found.")

# --- OPEN DASHBOARD ---
def open_dashboard():
    """Launch the Flask web dashboard."""
    try:
        speak("Opening web dashboard")
        os.system("python app.py")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open dashboard:\n{e}")

# --- GUI DESIGN ---
root = tk.Tk()
root.title("AttendX – Smart Attendance System")
root.geometry("450x420")
root.configure(bg="#2b2b2b")

# --- TITLE ---
title = tk.Label(root, text="AttendX", font=("Helvetica", 26, "bold"),
                 bg="#2b2b2b", fg="#00ff88")
title.pack(pady=10)

# --- CLOCK DISPLAY ---
clock_label = tk.Label(root, text="", font=("Consolas", 12, "bold"),
                       bg="#2b2b2b", fg="#00ff88")
clock_label.pack(pady=5)
update_clock()  # start updating time

# --- BUTTONS ---
btn1 = tk.Button(root, text="🎥 Start Live Camera", font=("Arial", 13, "bold"),
                 bg="#00ff88", fg="black", width=25, command=start_camera_mode)
btn1.pack(pady=8)

btn2 = tk.Button(root, text="🖼️ Upload Group Photo", font=("Arial", 13, "bold"),
                 bg="#00ff88", fg="black", width=25, command=select_photo_mode)
btn2.pack(pady=8)

btn3 = tk.Button(root, text="🌐 Open Web Dashboard", font=("Arial", 13, "bold"),
                 bg="#00ff88", fg="black", width=25, command=open_dashboard)
btn3.pack(pady=8)

# --- STATUS LABEL ---
status_label = tk.Label(root, text="🚀 Ready. Load faces or start camera.",
                        font=("Arial", 11), bg="#2b2b2b", fg="#00ff88")
status_label.pack(pady=15)

# --- FOOTER ---
footer = tk.Label(root, text="Press 'q' in camera window to quit",
                  font=("Arial", 10), bg="#2b2b2b", fg="#aaaaaa")
footer.pack(pady=5)

print("🚀 GUI launching... Please wait for the window to appear.")
root.mainloop()
