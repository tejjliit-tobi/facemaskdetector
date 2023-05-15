import os
#import webcam
import streamlit as st
import cv2
from configu import *
#from sampleImage.detect_mask_image import detect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
#from converter import convert_video
from detect_mask_video import video

st.set_page_config(
        page_title="FMD System",
)
#removed footer and headers
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

        
tab1, tab2, tab3, tab4 = st.tabs(["Home", "Dataset", "Instruction", "About"])

with tab1:
    st.title(PROJECT_NAME)
    st.info('''The Face Mask Detection Platform is powered by Artificial Neural Networks, enabling it to detect whether individuals are wearing masks or not. The application is compatible with both existing and new cameras, making it easy to identify people who are not wearing masks. By utilizing a face mask detection technique, we can encourage individuals to wear masks, thus reducing the spread of COVID-19 and other viral diseases.''')
    
    with st.container():
        st.title('')
        cnf = st.slider('Confidence threshold',min_value=.1, max_value=1.0,value=.5)
        st.info("Slide the bar left to right to adjust the camera confidence threshold.")
        btn = st.button("Start windows camera")
        if btn:
            video(cnf=cnf)

        st.title('')
        st.info("Sample video demo")
        video_file = open('videos/intro.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

   
   
with tab2:
    st.title("Sample Datasets")
    st.info('''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.''')
    
    st.header("Without mask")
    #st.image('image/about.jpg')
        
    st.header("Improper use of Mask")
    #st.image('image/about.jpg')

    st.header("With mask")
    #st.image('image/about.jpg')

with tab3:
    st.title("How to use Face Mask Detector System")
    st.info('''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.''')
    
    st.title("HOW TO USE THE SYSTEM")
    st.info('''Step 1. Connect your camera into your computer.\n''')
    st.image('instruction_images/a.png')
    st.info('''Step 2. Navigate to Home section.\n''')
    st.image('instruction_images/b.png')
    st.info('''Step 3. Adjust the camera confidence threshold.''')
    st.image('instruction_images/c.png')
    st.info('''Step 4. Click on the Start windows camera.''')
    st.image('instruction_images/d.png')
    st.info('''Then we're done!''')


with tab4:
    st.title(PROJECT_NAME)
    st.info('''The Face Mask Detection Platform is powered by Artificial Neural Networks, enabling it to detect whether individuals are wearing masks or not.''')
    st.write(DONE_BY)
 
