# Attendance Project

## 🎯 Overview
This project is an **Automated Attendance Management System** built using **Face Recognition**, **Flask API**, and a **Database**.  
It aims to record student/employee attendance automatically, detect spoofing attempts, and securely log the results for analysis.

---

## 📂 Project Structure
Attendance_Project/
├── Images/ # Sample images
├── Resources/ # Required resources
├── templates/ # Flask HTML templates
├── trained_models/ # Pre-trained models and encodings
├── FlaskAPI.py # Flask API server
├── main.py # Main script to run attendance
├── database.py # Database-related operations
├── encodeGenerator.py # Face encoding generator
├── with_antiSpoofing.py # Anti-spoofing module
├── serviceAccountKey.json # External service credentials (if used)
├── updated_students.json # Student information
├── dataLogger.xlsx # Attendance logs (Excel)
├── requirements.txt # Required Python packages
└── README.md # Project documentation


---

## ✨ Features
- **Face Recognition** based user identification  
- **Anti-Spoofing** to detect fake images or photos  
- **Flask API** endpoints to add, update, and fetch attendance records  
- **Database Integration** (Firebase support)  
- **Attendance Logs** stored in Excel  
- **Web Interface (Flask Templates)** for easy interaction  

---

## 🛠️ Requirements
- Python 3.x  
- Packages listed in `requirements.txt`  
- A working camera or video feed  
- (Optional) Firebase/External credentials if using `serviceAccountKey.json`  

---

