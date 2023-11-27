import cv2
import os
import streamlit as st
st.set_page_config(
    page_title="Create Dataset",
    page_icon= "🔨",
)
st.title("Create Dataset 🔨")

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
activated = st.toggle("Start Capturing")
if activated:
    #takin user id input
    face_id = st.text_input("Enter your ID:")

    # Start capturing video
    vid_cam = cv2.VideoCapture(0)
    st.write("Capturing")

    # Detect object in video stream using Haarcascade Frontal Face
    face_detector = cv2.CascadeClassifier('C:/Users/Lenovo/AppData/Local/Programs/Python/Python311/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

    # Initialize sample face image
    count = 0

    assure_path_exists("D:/Study/Coding/Projects/Mini Project/main/Dataset/")

    # Start looping
    while (True):

        # Capture video frame
        _, image_frame = vid_cam.read()

        # Convert frame to grayscale
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

        # Detect frames of different sizes, list of faces rectangles
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        # Loops for each faces
        for (x, y, w, h) in faces:
            # Crop the image frame into rectangle
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

        # If image taken reach 100, stop taking video
        elif count >= 50:
            st.success("Successfully Captured")
            break

    # Stop video
    vid_cam.release()

    # Close all started windows
    cv2.destroyAllWindows()
else:
    st.info("Video capturing is not turned on")