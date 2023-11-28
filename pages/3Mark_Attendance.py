import cv2
import numpy as np
import time
import streamlit as st
import sys
sys.path.append('D:\Study\Coding\Projects\Mini Project\main')
import xlwrite

st.set_page_config(
    page_title="Mark Attendance",
    page_icon= "📝",
)

st.title("Attendance Marking System 📝")
attendance_marked = False
start = time.time()
period = 8
detector = cv2.CascadeClassifier('C:/Users/Lenovo/AppData/Local/Programs/Python/Python311/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

activated = st.toggle("Start attendance marking system")

if activated:    
    cap = cv2.VideoCapture(0)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('D:/Study/Coding/Projects/Mini Project/main/Trainer/trainer.yml')

    flag = 0# a counter for failure in detection
    id = 0
    filename = 'filename'
    dict = {
        'item1': 1
    }

    #loading a font type
    font = cv2.FONT_HERSHEY_SIMPLEX
    found = False
    st.info("Recognising...")
    while True:
        
        #read a frame from the video
        ret, img = cap.read()
        
        #convert the frame to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        #detect the faces in the frame
        faces = detector.detectMultiScale(gray, 1.3, 5)
        
        #loop to iterate through the list f detected faces in image
        # (x, y, w, h) represents the coordinates and dimensions of each detected face rectangle:
        # x: X-coordinate of the top-left corner of the face rectangle
        # y: Y-coordinate of the top-left corner of the face rectangle
        # w: Width of the face rectangle
        # h: Height of the face rectangle
        for (x, y, w, h) in faces:
            
            #detecting the region of interest in the whole image
            roi_gray = gray[y:y + h, x:x + w]
            
            #draw a rectangle around the region of interest 
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            #get the id and the confidence value for the given roi_gray frame by matching it with the trained data
            #lower value of confidence indicates higher confidence
            id, confidence = recognizer.predict(roi_gray)                      
            #check if confidence is high
            if (confidence < 50):
                #match corresponding ids
                if (id == 1):
                    id = 'Aman'
                    found = True                    
                    #check if attendance is not already marked
                    if ((str(id)) not in dict):
                        filename = xlwrite.output('attendance', 'class1', 1, id, 'yes')
                        dict[str(id)] = str(id)
                        attendance_marked = True
                if (id == 2):
                    id = 'Elon Musk'
                    found = True                    
                    #check if attendance is not already marked
                    if ((str(id)) not in dict):
                        filename = xlwrite.output('attendance', 'class1', 2, id, 'yes')
                        dict[str(id)] = str(id)
                        attendance_marked = True

            else:
                id = 'Unknown, can not recognize'
                flag = flag + 1
                break
            
            #display text over the frame
            cv2.putText(img, str(id) + " " + str(confidence), (x, y - 10), font, 0.55, (120, 255, 120), 1)
            
        cv2.imshow('frame', img)#frame is the name of the window where image will be displayed
        
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
        if(found == False):
            st.warning("Mathch not found.")
        st.error("Attendance not marked")
    cap.release()
    cv2.destroyAllWindows()
else:
    st.info("Attendace marking system is off")