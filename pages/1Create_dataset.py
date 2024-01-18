import cv2
import os
import streamlit as st
st.set_page_config(
    page_title="Create Dataset",
    page_icon= "📷",
)
st.title("Create Dataset 📷")

#function to check if the specified  path for the folder where images will be stored exists or not 
#if the folder doesnot exist there, we create a new folder
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        
#use steramlit to make a toggle button to start capturing
activated = st.toggle("Start Capturing")

if activated:
    #taking user id input
    face_id = st.text_input("Enter your ID:")

    # Start capturing video
    vid_cam = cv2.VideoCapture(0)
    st.info("Capturing..")

    # Detect object in video stream using Haarcascade Frontal Face
    #cv2.CascadeClassifier initialises the cascade classifier object in openCV
    #argument specifies th epath to the XML file containing the pre trained model for detecting frontal faces
    face_detector = cv2.CascadeClassifier('C:/Users/Lenovo/AppData/Local/Programs/Python/Python311/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

    # Initialize counter fo the count of samples collected
    count = 0

    #verify that the given path exists, else creatte the needed folder
    assure_path_exists("D:/Study/Coding/Projects/Mini Project/main/Dataset/")

    # Start looping
    while (True):

        # Read frame from a video stream, vid_cam
        _, image_frame = vid_cam.read()

        # Convert frame to grayscale
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

        # Detect frames of different sizes, list of faces rectangles
        #If scaleFactor = 1.3, it shrinks the image by 30% for each scale.
        #minNeighbors = 5 means that a rectangle (potential face) should have at least 5 neighbors to be considered a valid face detection.
        #faces = face_detector.detectMultiscale(gray, scale_factor, min_neighbours)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        # Loops for each faces
        for (x, y, w, h) in faces:
            # Crop the image frame into rectangle
            #visulaise the deteted face by drawing a blue box around it
            cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Increment sample face image
            count += 1

            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

            # Display the video frame, with bounded rectangle on the person's face
            cv2.imshow('frame', image_frame)

        # To stop taking video, press 'q' for at least 100ms
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

        # If image taken reach 50, stop taking video
        elif count >= 50:
            st.success("Successfully Captured")
            break

    # Stop video
    vid_cam.release()

    # Close all started windows
    cv2.destroyAllWindows()
else:
    st.info("Video capturing is not turned on")