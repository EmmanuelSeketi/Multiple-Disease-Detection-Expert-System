import streamlit as st
from PIL import Image
import numpy as np
import joblib
from streamlit_extras.colored_header import colored_header

# Load the pre-trained model
model = joblib.load("Models\MalariaCnn.sav")

# Define the image size expected by the model
image_size = (64, 64)

# Function to preprocess the uploaded image
def preprocess_image(image):
    img = image.resize(image_size)
    img_array = np.array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# Streamlit app
def malaria():
    st.title("Malaria Disease Diagnosis ")
    colored_header(
        label="",
        description="Upload thin blood smear image taken from a microscope",
        color_name= "red-70",
    )
    
    st.write("\n")
    st.write("\n")

    # Upload image through Streamlit
    col1, col2 = st.columns([2, 1])

    with col1:
        selection = st.radio("SELECT YOUR DETECTION METHOD", ["Upload Image", "Capture Image"])

        st.write("\n")
        
                
        if selection=="Upload Image":
            imageFile = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
            if imageFile:
                st.image(imageFile)
        elif selection == "Capture Image":
            imageFile = st.camera_input("Take a picture")
            if imageFile:
                st.write("imageFile")

    # Display the uploaded image and classification result
    if imageFile is not None:
        # Display the result
        with col2:
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
           
    
            st.write("Classifying...")
            img = Image.open(imageFile)
            img_array = preprocess_image(img)
            prediction = model.predict(img_array)

            # Display the result with styling
            if prediction[0][0] > 0.5:
                st.success(" No Malaria Parasite Detected!")
                st.write("\n")
                st.write("If the patient exhibits symptoms or if there are concerns about their health, further evaluation  is recommended, including additional diagnostic methods if necessary.")
            else:
            
                st.error(" Malaria Parasite Detected!")
                st.write("\n")    
                st.write("The system has detected malaria parasites in the blood smear image. While providing valuable insights, comprehensive diagnosis and personalized treatment are essential.")

# Run the Streamlit app
malaria()
