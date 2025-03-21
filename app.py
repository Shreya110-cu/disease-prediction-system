import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(
    page_title="Disease Prediction Dashboard",
    layout="wide",
    page_icon="🩺"
)

# Get the working directory of the script
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load the saved models
diabetes_model = pickle.load(open(f"{working_dir}/diabetes_model.sav", "rb"))
heart_disease_model = pickle.load(open(f"{working_dir}/heart_disease_model.sav", "rb"))
parkinsons_model = pickle.load(open(f"{working_dir}/parkinsons_model.sav", "rb"))
 
# Sidebar for navigation
with st.sidebar:
    st.title("Navigation")
    selected = option_menu(
        "Disease Prediction System",
        ["Home", "Diabetes Prediction", "Heart Disease Prediction", "Parkinson's Prediction"],
        icons=["house", "activity", "heart", "person"],
        menu_icon="hospital-fill",
        default_index=0
    )

# Home Page
if selected == "Home":
    st.title("Welcome to the Disease Prediction Dashboard")
    st.markdown("""
        This application uses Machine Learning models to predict:
        - Diabetes
        - Heart Disease
        - Parkinson's Disease
    """)
    st.image("image.png", use_container_width=True)
    st.write("Use the sidebar to navigate to specific prediction pages.")

# Diabetes Prediction Page
if selected == "Diabetes Prediction":
    st.title("Diabetes Prediction")
    st.write("Provide the following details for prediction:")

    # Input form
    with st.form("diabetes_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            Pregnancies = st.number_input("Number of Pregnancies", min_value=0, value=0)
            SkinThickness = st.number_input("Skin Thickness (mm)", min_value=0.0, value=0.0)
            DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", min_value=0.0, value=0.0)

        with col2:
            Glucose = st.number_input("Glucose Level (mg/dL)", min_value=0.0, value=0.0)
            Insulin = st.number_input("Insulin Level (mu U/ml)", min_value=0.0, value=0.0)
            Age = st.number_input("Age", min_value=0, value=20)

        with col3:
            BloodPressure = st.number_input("Blood Pressure (mm Hg)", min_value=0.0, value=0.0)
            BMI = st.number_input("BMI", min_value=0.0, value=0.0)

        submitted = st.form_submit_button("Predict")

        # Perform prediction
        if submitted:
            user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
            diab_prediction = diabetes_model.predict([user_input])

            if diab_prediction[0] == 1:
                st.error("The person is diabetic.")
            else:
                st.success("The person is not diabetic.")

# Heart Disease Prediction Page
if selected == "Heart Disease Prediction":
    st.title("Heart Disease Prediction")
    st.write("Provide the following details for prediction:")

    # Input form
    with st.form("heart_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Age", min_value=0, value=30)
            sex = st.selectbox("Sex", options=["Male", "Female"])
            cp = st.number_input("Chest Pain Type (0-3)", min_value=0, max_value=3, value=0)
            trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=0.0, value=120.0)

        with col2:
            chol = st.number_input("Cholesterol (mg/dL)", min_value=0.0, value=200.0)
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", options=["Yes", "No"])
            restecg = st.number_input("Resting ECG Results (0-2)", min_value=0, max_value=2, value=0)
            thalach = st.number_input("Maximum Heart Rate Achieved", min_value=0.0, value=150.0)

        with col3:
            exang = st.selectbox("Exercise-Induced Angina", options=["Yes", "No"])
            oldpeak = st.number_input("ST Depression Induced by Exercise", min_value=0.0, value=1.0)
            slope = st.number_input("Slope of the Peak Exercise ST Segment (0-2)", min_value=0, max_value=2, value=1)
            ca = st.number_input("Number of Major Vessels Colored (0-3)", min_value=0, max_value=3, value=0)
            thal = st.number_input("Thalassemia (0=Normal, 1=Fixed Defect, 2=Reversible Defect)", min_value=0, max_value=2, value=1)

        submitted = st.form_submit_button("Predict")

        # Perform prediction
        if submitted:
            user_input = [age, int(sex == "Male"), cp, trestbps, chol, int(fbs == "Yes"), restecg,
                          thalach, int(exang == "Yes"), oldpeak, slope, ca, thal]
            heart_prediction = heart_disease_model.predict([user_input])

            if heart_prediction[0] == 1:
                st.error("The person has heart disease.")
            else:
                st.success("The person does not have heart disease.")

# Parkinson's Prediction Page
if selected == "Parkinson's Prediction":
    st.title("Parkinson's Disease Prediction")
    st.write("Provide the following details for prediction:")

    # Input form
    with st.form("parkinsons_form"):
        features = [
            "MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)", "MDVP:Jitter(Abs)", "MDVP:RAP",
            "MDVP:PPQ", "Jitter:DDP", "MDVP:Shimmer", "MDVP:Shimmer(dB)", "Shimmer:APQ3", "Shimmer:APQ5",
            "MDVP:APQ", "Shimmer:DDA", "NHR", "HNR", "RPDE", "DFA", "spread1", "spread2", "D2", "PPE"
        ]

        user_input = []
        cols = st.columns(5)
        for i, feature in enumerate(features):
            with cols[i % 5]:
                value = st.number_input(feature, min_value=0.0, value=0.0)
                user_input.append(value)

        submitted = st.form_submit_button("Predict")

        # Perform prediction
        if submitted:
            parkinsons_prediction = parkinsons_model.predict([user_input])

            if parkinsons_prediction[0] == 1:
                st.error("The person has Parkinson's disease.")
            else:
                st.success("The person does not have Parkinson's disease.")
