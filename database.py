import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import os

# Set working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred , {
    "databaseURL": "https://face-attendance-10774-default-rtdb.firebaseio.com/"
})
# Reference to the database
ref = db.reference("Students")

# Data to be inserted
students = [
    {"id": "104", "name": "Shristi Dixit", "branch": "ECE", "year": "3rd year", "total_attendence": 0},
    {"id": "101", "name": "Pranjal Mishra", "branch": "ECE", "year": "3rd year", "total_attendence": 0},
    {"id": "107", "name": "Divyanshi Sonkar", "branch": "ECE", "year": "3rd year", "total_attendence": 0},
    {"id": "103", "name": "Priyanshu Kashyap", "branch": "ECE", "year": "3rd year", "total_attendence": 0},
    {"id": "108", "name": "Priyanshu Chaudhary", "branch": "ECE", "year": "3rd year", "total_attendence": 0},
    {"id": "105", "name": "Anjali Sharma", "branch": "ECE", "year": "3rd year", "total_attendence": 0},
    {"id": "102", "name": "Vedath Batham", "branch": "ECE", "year": "3rd year", "total_attendence": 0},
    {"id": "106", "name": "Akarsh Tiwari", "branch": "ECE", "year": "3rd year", "total_attendence": 0}
]
data = {}
for student in students:
    data[student["id"]] = {
        "name": student["name"],
        "branch": student["branch"],
        "year": student["year"],
        "total_attendence": student["total_attendence"],
        "last_attendence_date": datetime.datetime(2025, 1, 1, 12, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
    }

# Write data to Firebase
for key, value in data.items():
    ref.child(key).set(value)

print("Data successfully uploaded to Firebase!")
