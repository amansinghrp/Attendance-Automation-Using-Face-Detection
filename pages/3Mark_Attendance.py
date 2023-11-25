import cv2
import numpy as np
import time
import streamlit as st
import sys
sys.path.append('D:\Study\Coding\Projects\Mini Project\main')
import xlwrite

st.title("Attendance Marking System")

st.write("Recognising...")
attendance_marked = False

start = time.time()
period = 8
face_cas = cv2.CascadeClassifier('C:/Users/Lenovo/AppData/Local/Programs/Python/Python311/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('D:/Study\Coding/Projects/Mini Project/main/Trainer/trainer.yml');
flag = 0
id = 0
filename = 'filename'
dict = {
    'item1': 1
}
#font = cv2.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 5, 1, 0, 1, 1)
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cas.detectMultiScale(gray, 1.3, 7)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        id, conf = recognizer.predict(roi_gray)
        with st.container():
            st.write("ID: ", id)
        if (conf < 50):
            if (id == 1):
                id = 'Aman'
                if ((str(id)) not in dict):
                    filename = xlwrite.output('attendance', 'class1', 1, id, 'yes')
                    dict[str(id)] = str(id)
                    attendance_marked = True
            if (id == 2):
                id = 'Elon Musk'
                if ((str(id)) not in dict):
                    filename = xlwrite.output('attendance', 'class1', 2, id, 'yes')
                    dict[str(id)] = str(id)
                    attendance_marked = True

        else:
            id = 'Unknown, can not recognize'
            flag = flag + 1
            break

        cv2.putText(img, str(id) + " " + str(conf), (x, y - 10), font, 0.55, (120, 255, 120), 1)
        
    cv2.imshow('frame', img);
    
    if flag == 10:
        st.error("Transaction Blocked")
        attendance_marked = False
        break
    if time.time() > start + period:
        break
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
if attendance_marked:
    st.success("Attendance Marked")
else:
    st.error("Attendance not marked")
cap.release()
cv2.destroyAllWindows()
