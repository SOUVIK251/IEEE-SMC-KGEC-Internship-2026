# AI-POWERED PRESCRIPTION READER
This project is an AI- based application which used to extract details from the medical prescription using OCR and AI- techniques

# FEATURES
- extract information from typed and scanned prescription
- supports handwritten recognition not fully
- extracts details directly from the typed and scanned pdf 
- for handwritten for miscorrection in typed text recognition  then OCR is used 
- extract patient details name, age , gender, doctor, hospital 
- medicine extraction and correction is done 
- the generates the structured report output of the extracted details in the format of pdf, json and text

# PREREQUISITES
-  Python
- Streamlit
- Tesseract OCR
- TrOCR
- OpenCV
- spaCy
- Transformers
- PDFPlumber
- PDF2Image
- RapidFuzz

# REQUIREMENTS
open VS code app , go to project folder
create and activate a virtual environment 
```Bash
python -m venv venv
```
# INSATLLATION PYTHON DEPEDENCIES 
install the required packages 
```bash 
pip install -r requirements.txt
```
external software required
```bash
pip install pytesseract pillow
pip install pdf2image
python -m spacy download en_core_web_sm
```
In ocr.py , update the pathway of tesseract and poppler according to your installation location on your computer

# HOW TO RUN 
```Bash
streamlit run app.py
```

# PROJECT STRUCTURE
app.py – Streamlit user interface
main.py – Main processing workflow
ocr.py – OCR and TrOCR processing
extractor.py – Medicine information extraction
ai_corrector.py – Medicine name correction
patient_parser.py – Patient detail extraction
report_generator.py – Report generation
medicine_database.csv – Medicine database
trocr_test.py – TrOCR testing
requirements.txt – Required Python packages

# THE GENERATED OUTPUT
the ouputs are stored in output/ folder
output/
- report.txt
- report.json
- report.pdf

# LIMITATIONS
-OCR accuracy depends on the quality of the input prescription.
-Poor-quality scans may produce incorrect text.
-Handwritten prescription recognition is not reliable for every handwriting style.
-TrOCR may produce incorrect results for unclear or complex handwriting.
-Medicine correction is limited to the medicines available in the reference database.
-Tesseract OCR and Poppler require separate installation and local path configuration.

# FUTURE SCOPE
- implementing the suitable AI- based Model for handwritten prescription
- Expanding the medicine database.
- Improving OCR preprocessing.
- Improving medicine-name correction.
- Improving patient information extraction.
- Testing on larger and more diverse datasets.
- Developing mobile or cloud-based versions.

# AUTHOR 
MUSKAN KHATOON
IEEE SMC SBC KGEC Research Internship Programme 2026