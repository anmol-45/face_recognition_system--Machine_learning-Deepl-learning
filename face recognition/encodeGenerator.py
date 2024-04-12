import cv2
import pickle
import os

import face_recognition

folderPath = 'images'
pathList = os.listdir(folderPath)
imgList = []
studentIds = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

# generating encoding list
def findEncoding(imageList):
    encodeList = []
    for img in imageList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("encoding started")
# calling the function findEncoding()
encodedList = findEncoding(imgList)
encodedList_withIds = [encodedList, studentIds]
print("encoding completed")
# Creating  a pickle file
file = open("encodeFile.p", 'wb')
pickle.dump(encodedList_withIds, file)
file.close()
print("File Saved")
