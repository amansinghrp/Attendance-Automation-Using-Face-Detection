import streamlit as st
import pandas as pd
import os

try:
    # Path to the folder where the attendance Excel files are stored
    attendance_folder = 'D:/Study/Coding/Projects/Mini Project/main/attendance/'
except Exception as e:
    print(e)
      
try:
    # Get a list of all Excel files in the attendance folder
    files = os.listdir(attendance_folder)
    excel_files = ["None"]+[file for file in files if file.endswith('.xls')]
except Exception as e:
    print(e)
    
# Let the user select the file to display
selected_file = st.selectbox('Select attendance sheet', excel_files)
attendance_folder = "D:/Study/Coding/Projects/Mini Project/main/attendance"  

file_path = os.path.join(attendance_folder, selected_file)

if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    df = pd.read_excel(file_path)
    st.write(df)
else:
    st.warning(f"The attendance sheet '{selected_file}' is either empty or does not exist.")
