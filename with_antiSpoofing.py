import os
import cv2
import torch
import pickle
import numpy as np
import pandas as pd
import datetime
from PIL import Image
from torchvision import transforms
import face_recognition
import firebase_admin
from firebase_admin import credentials, db

# -----------------------------
# Setup Paths & Working Directory
# -----------------------------
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# -----------------------------
# Firebase Initialization
# -----------------------------
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://face-attendance-10774-default-rtdb.firebaseio.com/"
})

# -----------------------------
# Device & Anti-Spoofing Model Loader
# -----------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = "trained_models/antispoof_fullmodels.pkl"

def load_models():
    models_dict = torch.load(model_path, map_location=device, weights_only=False)
    for name, model in models_dict.items():
        model.to(device)
        model.eval()
    return models_dict

models_dict = load_models()  # Load once at start

# Transform for anti-spoofing input
transform = transforms.Compose([
    transforms.Resize((160, 160)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

def is_real_face(face_img):
    """Returns True if face is real, False if spoof."""
    pil_img = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
    img_tensor = transform(pil_img).unsqueeze(0).to(device)
    probs_sum = None

    with torch.no_grad():
        for name, model in models_dict.items():
            output = model(img_tensor)
            probs = torch.softmax(output, dim=1)
            probs_sum = probs if probs_sum is None else probs_sum + probs

    avg_probs = probs_sum / len(models_dict)
    pred_class = torch.argmax(avg_probs, dim=1).item()
    return pred_class == 1  # 1 = real, 0 = spoof

# -----------------------------
# Load Face Encodings
# -----------------------------
with open("ENcodedFile.p", "rb") as file:
    encodeAndIdList = pickle.load(file)
encode, studentIDs = encodeAndIdList

# -----------------------------
# Function to Process Group Photo
# -----------------------------
def process_group_photo(group_photo_path):
    if not os.path.exists(group_photo_path):
        print(f"Error: Image not found at {group_photo_path}")
        return

    img = cv2.imread(group_photo_path)
    if img is None:
        print(f"Error: Failed to read image at {group_photo_path}")
        return

    img_small = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(img_small)
    face_encodings = face_recognition.face_encodings(img_small, face_locations)

    if not face_encodings:
        print("No faces detected in the group photo.")
        return

    for encoding, location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(encode, encoding)
        face_distances = face_recognition.face_distance(encode, encoding)
        match_index = np.argmin(face_distances)

        if matches[match_index]:
            student_id = studentIDs[match_index]
            print(f"Match found for student ID: {student_id}")

            # Crop face for anti-spoofing
            top, right, bottom, left = [v*4 for v in location]
            face_crop = img[top:bottom, left:right]

            if not is_real_face(face_crop):
                print(f"Spoof detected for student {student_id}. Attendance NOT marked.")
                continue

            # Fetch student info from Firebase
            student_info = db.reference(f"Students/{student_id}").get()
            if student_info is None:
                print(f"Student ID {student_id} not found in Firebase.")
                continue

            last_attendance = student_info.get("last_attendence_date")
            if not last_attendance:
                last_attendance = "2000-01-01 00:00:00"

            last_attendance_dt = datetime.datetime.strptime(last_attendance, "%Y-%m-%d %H:%M:%S")
            time_diff = (datetime.datetime.now() - last_attendance_dt).total_seconds()

            if time_diff > 10:
                student_info["total_attendence"] = student_info.get("total_attendence", 0) + 1
                student_info["last_attendence_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db.reference(f"Students/{student_id}").set(student_info)
                print(f"Attendance updated for {student_info.get('name', student_id)}. Total attendance: {student_info['total_attendence']}")
            else:
                print(f"Already marked attendance recently for {student_info.get('name', student_id)}. Skipping update.")

            # Update DataLogger
            if os.path.exists("datalogger.xlsx"):
                existing_df = pd.read_excel("datalogger.xlsx", sheet_name="Sheet1")
            else:
                existing_df = pd.DataFrame(columns=["Student_IDs", "Names", "Attendence_count", "Attempt_time"])

            new_data = {
                "Student_IDs": [student_id],
                "Names": [student_info.get("name", student_id)],
                "Attendence_count": [student_info["total_attendence"]],
                "Attempt_time": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            }
            new_df = pd.DataFrame(new_data)
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)

            with pd.ExcelWriter("datalogger.xlsx", mode="w", engine="openpyxl") as writer_file:
                updated_df.to_excel(writer_file, sheet_name="Sheet1", index=False)

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    group_photo_path = "group_photo_sample.jpg"
    process_group_photo(group_photo_path)
