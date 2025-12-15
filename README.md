
# AttendX
An automated attendance system using OpenCV and face recognition techniques. The system detects and recognizes multiple faces from a live camera or uploaded class photo, marks attendance automatically, and stores timestamped logs. It reduces manual effort, improves accuracy, and ensures efficient attendance management.

📸 Face Recognition–Based Attendance System (OpenCV)
📌 Project Overview

This project is an automated attendance management system built using OpenCV and face recognition techniques. It detects and recognizes multiple faces from a live camera feed or a single uploaded class photo, marks attendance automatically, and maintains timestamped attendance logs.

✨ Features

✔ Automatic attendance using face metrics
✔ Recognizes multiple students in a single image
✔ Supports image upload for class-wide attendance
✔ Real-time face detection and recognition
✔ Secure and accurate face matching
✔ Attendance logs with date & time
✔ Eliminates manual attendance errors

🧠 Technologies Used

Programming Language: Python

Computer Vision: OpenCV

Face Recognition: Face encodings & distance metrics

Data Storage: CSV / Database (attendance logs)

Image Processing: NumPy

⚙️ How It Works

Student face data is captured and stored as reference encodings.

A live camera feed or uploaded class image is processed.

Faces are detected and compared using facial metrics.

Recognized students are marked Present automatically.

Attendance is saved with date and time in log files.

📂 Attendance Logs

Student Name

Attendance Status

Date

Time

Example:

John_Doe | Present | 2025-09-12 | 09:45 AM

🚀 Installation & Usage

Clone the repository:

git clone https://github.com/your-username/face-attendance-opencv.git


Install dependencies:

pip install opencv-python face-recognition numpy


Run the project:

python main.py


Upload a class image or start live camera detection.

🔐 Privacy & Security

Face data is stored locally

No cloud upload or third-party sharing

Designed strictly for educational use

🎯 Use Cases

Classroom attendance automation

Colleges & universities

Training centers

Smart campus systems

⚠️ Limitations

Requires good lighting conditions

Accuracy depends on image quality

TO RUN:
python gui_attendance.py 
enter it in the terminal and run