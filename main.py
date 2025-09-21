import cv2
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

cap = cv2.VideoCapture(0)


#database Url
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred , {
    "databaseURL": "https://face-attendance-10774-default-rtdb.firebaseio.com/"
})


# setting camera

cap.set(3,640)
cap.set(4,480)

#importing BG and modes
imgBG = cv2.imread(r"C:\Users\Asus\Desktop\VS CODES\AttendenceProject\Resources\background.png")

ModePath = "Resources/Modes"
modePathList = os.listdir(ModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(ModePath , path)))



# loading the encode]ing file
with open("ENcodedFile.p","rb") as file:
    encodeAndIdlist = pickle.load(file)
encode , IDs = encodeAndIdlist

modeType = 0
counter = 0
id = -1

# checking user choice
print("1 for group attendence  - 0 for individual attendence")
#choice = int(input("enter your choice as 0 or 1 "))

# building window
while True:
    success , img = cap.read()
     
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS , cv2.COLOR_BGR2RGB)

    faceCurrent = face_recognition.face_locations(imgS)
    encodeCurrentFace = face_recognition.face_encodings(imgS,faceCurrent)

    imgBG[162:162+480,55:55+640] = img
    imgBG[44:44+633,808:808+414] = imgModeList[modeType]

    if faceCurrent:
        

        # face matching
        for e, l in zip(encodeCurrentFace , faceCurrent):
            matches = face_recognition.compare_faces(encode,e)
            faceDis = list(face_recognition.face_distance(encode,e))
            # print("face distance ", faceDis)
            # print("mathing ", matches)
            matchINDEX = np.argmin(faceDis)
            if matches[matchINDEX]:
                y1,x2,y2,x1 = l
                y1,x2,y2,x1 = y1 *4,x2 *4,y2 *4,x1 *4
                bbox =  55+x1 , 162+y1 ,x2-x1 , y2-y1
                imgBg = cvzone.cornerRect(imgBG,bbox,rt=0)
                id = IDs[matchINDEX]

                if counter ==0:
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                studentInfo = db.reference(f"Students/{id}").get()
                print(studentInfo)

                #updating attendence
                datetimeObject = datetime.strptime(studentInfo["last_attendence_date"],"%Y-%m-%d %H:%M:%S")
                timeDiff = (datetime.now() - datetimeObject).total_seconds()

                if timeDiff > 10:
                    ref = db.reference(f"Students/{id}")
                    studentInfo["total_attendence"] += 1
                    ref.child("total_attendence").set(studentInfo["total_attendence"])
                    ref.child("last_attendence_date").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBG[44:44+633,808:808+414] = imgModeList[modeType]

            if modeType != 3:  

                if 10<counter<20:
                    modeType = 2

                if counter <= 10:
                    cv2.putText(imgBG,str(studentInfo["total_attendence"]),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    cv2.putText(imgBG,str(studentInfo["name"]),(808,445),cv2.FONT_HERSHEY_COMPLEX,0.5,(25,25,25),1)
                    cv2.putText(imgBG,str(studentInfo["branch"]),(1000,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgBG,str(id),(1000,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)

                counter +=1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgBG[44:44+633,808:808+414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0


    #cv2.imshow("Camera", img)
    cv2.imshow("Face Attendence" , imgBG)
    cv2.waitKey(1)

    if cv2.getWindowProperty("Face Attendence", cv2.WND_PROP_VISIBLE) < 1:
        break