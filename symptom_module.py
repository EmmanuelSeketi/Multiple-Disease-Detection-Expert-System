import streamlit as st
import joblib
from streamlit_extras.colored_header import colored_header
# Load the trained model
model = joblib.load("Models\symptom.sav")

# Original list of symptoms
l1_original = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
               'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
               'spotting_urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings',
               'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough',
               'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache',
               'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain',
               'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes',
               'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise',
               'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure',
               'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate',
               'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain',
               'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes',
               'enlarged_thyroid', 'brittle_nails', 'swollen_extremities', 'excessive_hunger', 'extra_marital_contacts',
               'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck',
               'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
               'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of_urine',
               'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression',
               'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
               'abnormal_menstruation', 'dischromic_patches', 'watering_from_eyes', 'increased_appetite', 'polyuria',
               'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances',
               'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
               'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum',
               'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring',
               'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
               'red_sore_around_nose', 'yellow_crust_ooze']

# List of diseases
disease = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction',
           'Peptic ulcer disease', 'AIDS', 'Diabetes', 'Gastroenteritis', 'Bronchial Asthma', 'Hypertension',
           'Migraine', 'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 'Jaundice', 'Malaria', 'Chicken pox',
           'Dengue', 'Typhoid', 'hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E',
           'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemorrhoids(piles)',
           'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthritis',
           'Arthritis', '(vertigo) Paroxysmal Positional Vertigo', 'Acne', 'Urinary tract infection', 'Psoriasis',
           'Impetigo']

# Streamlit app
def symptome():
    st.title("Symptom-based Disease Diagnosis")
    colored_header(
        label=" ",
        description="Select various symptoms from side bar to detect disease based on those symptoms",
        color_name= "red-70",
    )
    st.write("\n")  
      
    import json
    from streamlit_lottie import st_lottie
    def load_lottiefile(filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    lottiedoc = load_lottiefile("LottieFiles\Symptoms.json")
    #st_lottie(
        #lottiedoc,
        #speed=0.6, 
        #loop=True,
       # quality="high",
        #height=200,
       # width=500,
    
  #  )
    # Define your main content
    
    selected_symptoms = st.multiselect("Select symptoms", l1_original, key="selected_symptoms")
    st.write("\n")
    if not selected_symptoms:
        st.write("\n")
        st.warning("Please select at least one symptom to detect disease.")
        
        return

    # Define your main content
    if selected_symptoms:
        st.write("\n")
        
        prediction = predict_disease(selected_symptoms)
        st.subheader("Diagnosis:")
        st.error(prediction)

def predict_disease(symptoms):
    # Create an input array for prediction
    input_data = [1 if symptom in symptoms else 0 for symptom in l1_original]
    input_data = [input_data]  # Scikit-learn expects a 2D array

    # Make prediction using the trained model
    prediction = model.predict(input_data)[0]

    # Get the corresponding disease
    predicted_disease = disease[prediction]

    return predicted_disease

if __name__ == "__main__":
    symptome()
