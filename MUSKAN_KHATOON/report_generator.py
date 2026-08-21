# responsibile to create result in three formats - json,text,pdf
import json  # json
from reportlab.lib.pagesizes import letter   #pdf
from reportlab.pdfgen import canvas  #writing text onto the pdf

# save deatils as a text file
def save_txt(patient, medicines, filename="output/report.txt"):
# open text in write mode , utf-8 allows normal charatcters storing
    with open(filename, "w", encoding="utf-8") as f:

        f.write("AI PRESCRIPTION REPORT\n")
        f.write("=" * 50 + "\n\n")
        # from patient_parser.py
        f.write("PATIENT DETAILS\n")
        f.write(f"Patient Name : {patient['patient_name']}\n")
        f.write(f"Doctor       : {patient['doctor_name']}\n")
        f.write(f"Age          : {patient['age']}\n")
        f.write(f"Gender       : {patient['gender']}\n")
        f.write(f"Hospital     : {patient['hospital']}\n")
        f.write(f"Date         : {patient['date']}\n\n")

        f.write("MEDICINES\n")
        f.write("=" * 50 + "\n")

        for med in medicines:

            f.write(f"Medicine  : {med['corrected']}\n")
            f.write(f"Strength  : {med['strength']}\n")
            f.write(f"Dosage    : {med['dosage']}\n")
            f.write(f"Frequency : {med['frequency']}\n")
            f.write(f"Duration  : {med['duration']}\n")
            f.write(f"Confidence: {med['confidence']}%\n")
            f.write("-" * 50 + "\n")

# creates structured json report
def save_json(patient, medicines, filename="output/report.json"):
    data = {
        "patient": patient,
        "medicines": medicines
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)  

# creates pdf report
def save_pdf(patient, medicines, filename="output/report.pdf"):
    pdf = canvas.Canvas(filename, pagesize=letter)
    y = 760
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "AI Prescription Report")
    y -= 40
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Patient : {patient['patient_name']}")
    y -= 20
    pdf.drawString(50, y, f"Doctor : {patient['doctor_name']}")
    y -= 20
    pdf.drawString(50, y, f"Age : {patient['age']}")
    y -= 20
    pdf.drawString(50, y, f"Gender : {patient['gender']}")
    y -= 20
    pdf.drawString(50, y, f"Hospital : {patient['hospital']}")
    y -= 20
    pdf.drawString(50, y, f"Date : {patient['date']}")
    y -= 40
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Medicines")
    y -= 30
    pdf.setFont("Helvetica", 11)
    for med in medicines:
        pdf.drawString(50, y, f"Medicine : {med['corrected']}")
        y -= 18
        pdf.drawString(70, y, f"Strength : {med['strength']}")
        y -= 18
        pdf.drawString(70, y, f"Dosage : {med['dosage']}")
        y -= 18
        pdf.drawString(70, y, f"Frequency : {med['frequency']}")
        y -= 18
        pdf.drawString(70, y, f"Duration : {med['duration']}")
        y -= 18
        pdf.drawString(70, y, f"Confidence : {med['confidence']}%")
        y -= 30
        if y < 80:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = 760
    pdf.save()