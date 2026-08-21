# take ocr text -- identity medi names,dose,freq,duration
# extractor + ai corrector = medi details
import re
from ai_corrector import correct_medicine  

def extract_medicines(text): 
    medicines = []  # medi list
    lines = text.split("\n") # split ocr text into lines

# loop search for medi line
    for line in lines:
        line = line.strip() # remove unnecessary space
        if not line:
            continue
        strength = re.search(
            r"\d+\s*(mg|mcg|g|ml)",
            line,
            re.IGNORECASE
        )
        if strength:
            current = {} # new dictiionary
            current["strength"] = strength.group()
            medicine = re.sub(
                r"^\d+\.\s*",
                "", # remove numbering
                line
            )
            medicine = re.sub(
                r"\d+\s*(mg|mcg|g|ml).*",
                "",
                medicine,
                flags=re.IGNORECASE
            ).strip()

            # send medi to ai_corrector
            current["medicine"] = medicine

            result = correct_medicine(medicine)

            current["corrected"] = result["corrected_name"]
            current["confidence"] = result["confidence"]
            current["status"] = result["status"]

            current["dosage"] = ""
            current["frequency"] = ""
            current["duration"] = ""

            medicines.append(current) # adds medi to the list

            continue

        # search for dosage
        dose = re.search(
            r"(\d+)\s*(tablet|tablets|capsule|capsules|ml)",
            line,
            re.IGNORECASE
        )

        if dose and medicines:
            medicines[-1]["dosage"] = dose.group()

        if medicines:
            frequency_patterns = [
                "once daily",
                "twice daily",
                "thrice daily",
                "daily",
                "morning",
                "night",
                "bedtime",
                "before food",
                "after food",
                "every morning",
                "every night"
            ]
            for f in frequency_patterns:
                if f.lower() in line.lower():
                    medicines[-1]["frequency"] = f

        # duration 
        duration = re.search(
            r"\d+\s*(day|days|week|weeks|month|months)",
            line,
            re.IGNORECASE
        )
        if duration and medicines:
            medicines[-1]["duration"] = duration.group()

    return medicines