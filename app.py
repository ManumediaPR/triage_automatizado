
import streamlit as st
import random
import json
import matplotlib.pyplot as plt

def generate_fake_data():
    return {
        "Height (in)": round(random.uniform(39.0, 78.0), 2),
        "Weight (lbs)": round(random.uniform(90.0, 265.0), 1),
        "Temperature (F)": round(random.uniform(96.8, 102.2), 1),
        "Blood Pressure": {
            "Systolic": random.randint(90, 140),
            "Diastolic": random.randint(60, 90)
        },
        "Oximeter": {
            "SpO2": random.randint(90, 100),
            "Pulse": random.randint(60, 100)
        }
    }

st.set_page_config(page_title="Automated Triage System", layout="centered")
st.title("🩺 Automated Triage System")
st.markdown("---")

with st.form("patient_form"):
    st.subheader("Patient Information")
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=0, max_value=120)

    reason_options = [
        "Respiratory issue", "Cardiac issue", "Chest pain", "Fall or trauma",
        "Abdominal pain", "Headache or migraine", "Fever or infection",
        "Dizziness or fainting", "Neurological symptoms", "Gastrointestinal problems",
        "Psychiatric or emotional issue", "Post-surgical follow-up or wounds",
        "Muscular or lower back pain", "Seizures", "Urinary or kidney problems",
        "Allergic reaction or insect bites", "Other"
    ]
    reason = st.selectbox("Reason for visit", reason_options)
    if reason == "Other":
        reason = st.text_input("Please specify the reason")

    pain_level = st.slider("Pain Level (1-10)", 1, 10)

    allergy_status = st.radio("Is the patient allergic to any medication?", ["No", "Yes"])
    allergy_info = "None"
    if allergy_status == "Yes":
        allergy_info = st.text_input("Which medication is the patient allergic to? Please type and press ENTER:")

    submitted = st.form_submit_button("Submit")

if submitted:
    st.success("Patient registered successfully!")
    sensor_data = generate_fake_data()

    patient_data = {
        "Name": name,
        "Age": age,
        "Reason for Visit": reason,
        "Pain Level": pain_level,
        "Allergies": allergy_info,
        **sensor_data
    }

    st.markdown("### Triage Summary")
    st.json(patient_data)

    # Blood pressure chart
    st.markdown("#### Blood Pressure")
    fig, ax = plt.subplots()
    ax.bar(["Systolic", "Diastolic"], [
        sensor_data["Blood Pressure"]["Systolic"],
        sensor_data["Blood Pressure"]["Diastolic"]
    ])
    st.pyplot(fig)

    # Oximeter chart
    st.markdown("#### Oximeter")
    fig2, ax2 = plt.subplots()
    ax2.bar(["SpO2", "Pulse"], [
        sensor_data["Oximeter"]["SpO2"],
        sensor_data["Oximeter"]["Pulse"]
    ])
    st.pyplot(fig2)

    # Save to JSON file
    with open("triage_report.json", "w") as f:
        json.dump(patient_data, f, indent=2)
    st.info("Triage data saved to 'triage_report.json'")
