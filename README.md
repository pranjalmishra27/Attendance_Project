# 🚀 Smart Attendance System (Face Recognition + Anti-Spoofing)

## 🎯 Overview
This project is an **Automated Attendance Management System** built using **Computer Vision** and **Machine Learning**. It leverages **face recognition with anti-spoofing** to securely mark attendance, eliminating manual processes and reducing errors.

The system uses a **custom curated dataset**, integrates a **Flask API**, and stores attendance records in a database for real-time access and analysis.

---

## 📊 Key Achievements
- ✅ Achieved **F1-score of 0.97** for face recognition  
- 🔒 Implemented **ResNet-based anti-spoofing (99% accuracy)** to block photo/video attacks  
- ⚡ Reduced manual attendance time by **~90% (from minutes to seconds)**  
- 📉 Eliminated proxy attendance and improved system reliability  

---

## ✨ Features
- 👤 **Face Recognition** for automated attendance marking  
- 🛡️ **Anti-Spoofing System** to detect fake faces (photos/videos)  
- 🌐 **Flask API** for managing attendance records  
- 🗄️ **Database Integration (Firebase supported)**  
- 📄 **Excel Logging System** for attendance tracking  
- 💻 **Web Interface (Flask Templates)** for user interaction  
- ⚡ **Real-time Processing** for fast and efficient performance  

---

## 🧠 Tech Stack
- **Language:** Python  
- **Libraries:** OpenCV, NumPy, Pandas, Scikit-learn  
- **Models:** MobileNetV2, ResNet18  
- **Framework:** Flask  
- **Database:** Firebase / JSON-based storage  
- **Tools:** Excel logging, custom dataset preprocessing  

---

## 📂 Project Structure
Attendance_Project
│
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
