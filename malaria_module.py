import streamlit as st
from PIL import Image
import numpy as np
import joblib
import os
from streamlit_extras.colored_header import colored_header

# Model will be loaded lazily to avoid import-time unpickling errors
model = None
model_candidates = [
    os.path.join(os.path.dirname(__file__), "Models", "MalariaCnn.sav"),
    os.path.join(os.path.dirname(__file__), "MalariaCnn.sav"),
]
model_path = next((p for p in model_candidates if os.path.exists(p)), model_candidates[0])


def _load_model():
    """Attempt to load the model and return it; on failure return None and
    a friendly error message.
    """
    global model
    if model is not None:
        return model, None
    if not os.path.exists(model_path):
        return None, f"Model file not found at {model_path}"
    try:
        mdl = joblib.load(model_path)
        model = mdl
        return model, None
    except ModuleNotFoundError as mnfe:
        # Common when pickled objects reference a keras internal path not present
        msg = (
            "Model unpickling failed due to missing module: "
            f"{mnfe.name}. This often happens when the model was pickled with a different Keras/TensorFlow version.\n"
            "Suggested fixes:\n"
            "  1) Recreate the model file using Keras/TensorFlow in your current environment (recommended).\n"
            "  2) Install a compatible TensorFlow/Keras version used to create the model. Example:\n"
            "       pip install 'tensorflow==2.11.0'\n"
            "     or try installing a matching Keras version:\n"
            "       pip install 'keras==2.11.0'\n"
            "  3) If you can't change the environment, re-save the model using Keras' native `model.save()` and load with `keras.models.load_model()` instead of pickling.\n"
        )
        return None, msg
    except Exception as e:
        return None, f"Failed to load model: {e}"

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

    # Load model at runtime (lazy)
    mdl, err = _load_model()
    if err:
        st.error(err)
        return

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
            prediction = mdl.predict(img_array)

            # Display the result with styling
            if prediction[0][0] > 0.5:
                st.success(" No Malaria Parasite Detected!")
                st.write("\n")
                st.write("If the patient exhibits symptoms or if there are concerns about their health, further evaluation  is recommended, including additional diagnostic methods if necessary.")
            else:
            
                st.error(" Malaria Parasite Detected!")
                st.write("\n")    
                st.write("The system has detected malaria parasites in the blood smear image. While providing valuable insights, comprehensive diagnosis and personalized treatment are essential.")

# Note: Do not call malaria() at import time. The Streamlit entrypoint should
# import this module and call malaria() when the user navigates to the page.
