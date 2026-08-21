import re # REGULAR EXPRESSION  to find patterns
import spacy # identity entites , give AI understanding

# Load small english spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_patient_details(text): # OCR text from main.py
    patient = {
        "patient_name": "",
        "doctor_name": "",
        "age": "",
        "gender": "",
        "date": "",
        "hospital": ""
    }

    doc = nlp(text)  #Spacy identity entities from ocr text
    persons = []

    # spaCy Detection
    for ent in doc.ents: # ent = entity detected

        if ent.label_ == "PERSON":
            persons.append(ent.text)

        elif ent.label_ == "ORG":
            if not patient["hospital"]:
                patient["hospital"] = ent.text

    # Patient Name
    match = re.search(
        r"(Patient\s*Name|Name)\s*[:\-]?\s*([A-Za-z ]+)",
        text,
        re.IGNORECASE
    )

    if match:

        patient["patient_name"] = match.group(2).strip()

    elif persons:

        patient["patient_name"] = persons[0]

    # Doctor Name
    
    doctor_match = re.search(
        r"(?:Doctor|Dr\.?)\s*[:\-]?\s*"
        r"((?:Dr\.?\s*)?[A-Za-z][A-Za-z .'-]*"
        r"(?:,\s*[A-Za-z.]+)*?)"
        r"(?=\s+(?:Department|Hospital|Patient\s*Name|Patient|Age|Gender|Date)\s*:|$)",
        text,
        re.IGNORECASE
    )

    if doctor_match:

        doctor_name = doctor_match.group(1).strip()
        doctor_name = re.sub(
            r"^Dr\.?\s*",
            "",
            doctor_name,
            flags=re.IGNORECASE
        )

        patient["doctor_name"] = doctor_name.strip()

    # Age
    age = re.search(
        r"Age\s*[:\-]?\s*(\d{1,3})",
        text,
        re.IGNORECASE
    )

    if age:
        patient["age"] = age.group(1) + " years"
    else:
        age = re.search(
            r"(\d{1,3})\s*(years|year|yrs|yr)",
            text,
            re.IGNORECASE
        )

        if age:
            patient["age"] = age.group()

    # Gender
    gender = re.search(
        r"\b(Male|Female|Other)\b",
        text,
        re.IGNORECASE
    )

    if gender:
        patient["gender"] = gender.group().title()

    # Hospital

    hospital = re.search(
        r"(Hospital|Clinic)\s*[:\-]?\s*(.+)",
        text,
        re.IGNORECASE
    )

    if hospital:

        patient["hospital"] = hospital.group(2).strip()

    # Date 
   
    date_patterns = [

        r"Date\s*[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",

        r"Date\s*[:\-]?\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})",

        r"Date\s*[:\-]?\s*([A-Za-z]+\s+\d{1,2},?\s+\d{4})"

    ]

    for pattern in date_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            patient["date"] = match.group(1).strip()

            break

    return patient