import os,cv2;
import numpy as np
from PIL import Image;
import streamlit as st
import time
st.set_page_config(
    page_title="Train Dataset",
    page_icon= "👷",
)

st.title("Train your Dataset 👷")

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector= cv2.CascadeClassifier("C:/Users/Lenovo/AppData/Local/Programs/Python/Python311/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml");

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    #create empth face list
    faceSamples=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces=detector.detectMultiScale(imageNp)
        #If a face is there then append that in the list as well as Id of it
        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(Id)
    return faceSamples,Ids

options = ['None','Yes', 'No']
choice = st.selectbox('Do you want to train the collected dataset?', options)
    
if choice == 'Yes':
    st.info("Locating file path..")
    path = r"D:/Study/Coding/Projects/Mini Project/main/Dataset"
    if os.path.exists(path):
        st.info("Training the data..")
        faces,Ids = getImagesAndLabels(path)
        s = recognizer.train(faces, np.array(Ids))
        recognizer.write('D:/Study\Coding/Projects/Mini Project/main/Trainer/trainer.yml')
        st.success("Successfully trained")
    else:
        st.error("File not found at the specified path.")
elif choice == 'No':
    st.info("Collected data is not trained yet")

