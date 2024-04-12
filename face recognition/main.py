import cv2
# import cvzone
import face_recognition
import pickle
import numpy as np
import cvzone

# Import the background image for the capture screen
imgBackground = cv2.imread('resources/A.png')

# Load the saved encodings from the pickle file
file = open("encodeFile.p", 'rb')
encodedList_withIds = pickle.load(file)
file.close()
encodedList, studentIds = encodedList_withIds

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

match_found = False
while cap.isOpened():
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Find faces in the current frame
    faceCurr = face_recognition.face_locations(imgS)
    encodeCurr = face_recognition.face_encodings(imgS, faceCurr)

    # Paste the captured frame onto the background image
    imgBackground[32:32 + 480, 55:55 + 640] = img

    # Compare each face in the current frame with the known faces
    for encodFace, faceLoc in zip(encodeCurr, faceCurr):
        matches = face_recognition.compare_faces(encodedList, encodFace)
        faceDis = face_recognition.face_distance(encodedList, encodFace)

        match_idx = np.argmin(faceDis)
        if matches[match_idx]:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 32 + x1, 55 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            print("student Detected: ", studentIds[match_idx])
            # match_found = True  # Set the flag to True
        else:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 32 + x1, 55 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0, colorC=(0, 0, 255))
            print("Cannot detect face")
            # match_found = True

    cv2.imshow("BackGround", imgBackground)

    cv2.waitKey(1)
    # if match_found:
    #     cv2.waitKey(38000)  # Wait for 3 seconds
    #     break  # Break out of the loop after 3 seconds

cap.release()
cv2.destroyAllWindows()