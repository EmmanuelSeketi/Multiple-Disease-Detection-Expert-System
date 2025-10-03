import streamlit as st
from streamlit_extras.colored_header import colored_header

def diabetes():
    # Header
    st.title("Diabetes Disease Diagnosis")
    colored_header(
        label="",
        description="Enter patient information to screen for  diabetes.",
        color_name="red-70",
    )
    
    
   
    st.write("\n")

  
    # Input Fields
   
    col1, col2, col3 = st.columns(3)
    with col1:
        pregnancies = st.text_input('Number of Pregnancies', placeholder="Your input")
        
    with col2:
        glucose = st.text_input('Glucose Level', placeholder="Your input")
    with col3:
        
        blood_pressure = st.text_input('Blood Pressure value', placeholder="Your input")
    with col1:
        skin_thickness = st.text_input('Skin Thickness value', placeholder="Your input")
    with col2:
        insulin = st.text_input('Insulin level', placeholder="Your input")
    with col3:
        bmi = st.text_input('BMI value', placeholder="Your input") 
    with col1:
        dpf = st.text_input('Diabetes Pedigree Function ', placeholder="Your input")          
    with col2:
        age = st.text_input('Age', placeholder="Your input")     
    
    st.write("\n")
    st.write("\n")
    st.write("\n")
   
    # Submit Button
    if st.button("Detect Diabetes"):
        # Placeholder for prediction logic
        st.success("Diabetes detection logic will be executed here.")
    
# Do not execute diabetes() on import. The Streamlit entrypoint will call diabetes()
