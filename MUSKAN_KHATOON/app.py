# its the front end , it create streamlit interface

import streamlit as st  # for interface 
import os

from main import process_prescription  # calls from main.py

st.set_page_config(  # front end appearance
    page_title="AI Prescription Reader",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 AI Powered Prescription Reader")   # main haeding

st.markdown(
    "Upload a **typed, scanned or handwritten prescription**."  # short detail or info ** for bold**
)

uploaded_file = st.file_uploader(  # func for uploadind file
    "Choose Prescription PDF",
    type=["pdf"]
)

if uploaded_file:
    with st.spinner("Processing Prescription."):
        patient, medicines, text = process_prescription(uploaded_file) # send uploaded file to main.py to extract details 

    st.success("Prescription Processed Successfully!")

    # OCR TEXT

    with st.expander("View OCR Output"): # for seeing the ocr output
        st.text(text)

    # PATIENT AND DOCTOR DETAILS comes from patient_parser.py

    st.header("👤 Patient Details")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(f"**Patient Name:** {patient['patient_name']}")
    # (f-string) that lets you inject variables directly into text using curly braces {}.
        st.markdown(f"**Age:** {patient['age']}")

        st.markdown(f"**Gender:** {patient['gender']}")

    with col2:

        st.markdown(f"**Doctor:** {patient['doctor_name']}")

        st.markdown(f"**Hospital:** {patient['hospital']}")

        st.markdown(f"**Date:** {patient['date']}")

    st.divider()

    # MEDICINES from extractor.py 

    st.header("💊 Medicines")

    if medicines:

        for i, med in enumerate(medicines, start=1): #looping

            with st.container():
                st.subheader(f"Medicine {i}")

                col1, col2 = st.columns(2)

                with col1:
                    # detected by OCR corrected by RapidFUzz
                    st.write("**Detected:**", med["medicine"])

                    st.write("**Corrected:**", med["corrected"])

                    st.write("**Strength:**", med["strength"])

                    st.write("**Dosage:**", med["dosage"])

                with col2:

                    st.write("**Frequency:**", med["frequency"])

                    st.write("**Duration:**", med["duration"])

                    st.write(
                        "**Confidence:**",
                        f"{med['confidence']}%"
                    )

                st.divider()

    else:

        st.warning("No medicines detected.")

    # DOWNLOADS

    st.header("📥 Reports")

    col1, col2, col3 = st.columns(3)

    with col1:

        with open("output/report.txt", "rb") as f:

            st.download_button( # button for text
                "Download TXT",
                f,
                "report.txt"
            )

    with col2:

        with open("output/report.json", "rb") as f: # button for json

            st.download_button(
                "Download JSON",
                f,
                "report.json"
            )

    with col3:

        with open("output/report.pdf", "rb") as f:  # button for pdf

            st.download_button(
                "Download PDF",
                f,
                "report.pdf"
            )