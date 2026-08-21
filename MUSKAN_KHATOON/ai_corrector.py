# handles medi name after correction
import pandas as pd #  panda for reading medi database_csv
from rapidfuzz import process  # fuzzy string matching the medi

# Loads Medicine Database
try:
    medicine_db = pd.read_csv("medicine_database.csv")
    if "Medicine" in medicine_db.columns:
        medicine_list = (
            medicine_db["Medicine"]
            .dropna()       # remove empty value
            .astype(str)    # converts value into text
            .str.strip()    # unnecessary space removes
            .tolist()        #converts the column into python list [pcm,taxim]
        )
    else:
        medicine_list = []
except Exception:
    medicine_list = []

# Correct One Medicine
def correct_medicine(name):
    if not name.strip():
        return {         
            "corrected_name": name,
            "confidence": 0,
            "status": "Unknown"
        }
    if len(medicine_list) == 0:  # check the database is available 
        return {         # if no medi loaded from database
            "corrected_name": name,
            "confidence": 0,
            "status": "Database Missing"
        }
    
# fuzzy matching
    match = process.extractOne(  # this function finds the closet medi
        query=name,
        choices=medicine_list,
        score_cutoff=50   # matching >= 50
    )
    if match:
        return {
            "corrected_name": match[0],
            "confidence": round(match[1], 2),
            "status": "Matched"
        }
    return {
        "corrected_name": name,
        "confidence": 0,
        "status": "Unknown"
    }

# Correct Entire Prescription , handles multiple medicines not just one
def correct_prescription(medicines):
    corrected = []   # create empty list
    for med in medicines:
        result = correct_medicine(
            med["medicine"]
        )
        med["corrected_name"] = result["corrected_name"]
        med["confidence"] = result["confidence"]
        med["status"] = result["status"]
        corrected.append(med)       # processed medi added to final list
        
    return corrected
