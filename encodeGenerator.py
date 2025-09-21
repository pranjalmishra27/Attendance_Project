import cv2
import face_recognition
import pickle
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"Current Working Directory: {os.getcwd()}")

folderPath = "Images"
PathList = os.listdir(folderPath)
imgList = []
studentID = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentID.append(os.path.splitext(path)[0])
print(studentID) 

def findEncoding(imagesList):
    encodingList = []
    for image in imagesList:
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encodingList.append(encode)
    return encodingList

with open("ENcodedFile.p","wb") as file :
    pickle.dump([findEncoding(imgList),studentID], file)
