# conroller send each ocr text into respective module
# connects the modules 

from ocr import extract_text
from patient_parser import extract_patient_details
from extractor import extract_medicines
from report_generator import save_txt, save_json, save_pdf


def process_prescription(uploaded_file): # process upload file

    # OCR
    text = extract_text(uploaded_file) # ocr text = text

    # Patient Details
    patient = extract_patient_details(text) # text pass to patient_parser.py then store back in patient

    # Medicines
    medicines = extract_medicines(text)

    # Reports
    save_txt(patient, medicines)

    save_json(patient, medicines)

    save_pdf(patient, medicines)

    return patient, medicines, text # return to app.py 