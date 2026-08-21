 # full ocr pipeline 
import pdfplumber # extract directly text from typed pdfs
import pytesseract   #performs ocr on images using tesseract
import cv2  #opencv image processing
import numpy as np   #conerts images as arrays
import torch   #runs TrOCR deep-learning model

from pdf2image import convert_from_bytes  # convert pdf = images
from PIL import Image   # pillow is used here for image handling

from transformers import (
    TrOCRProcessor,
    VisionEncoderDecoderModel
)

# Tesseract OCR Path
# TEsseract needs to installed separately by users
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\Others\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)

# Poppler Path , poppler is required by pdf2image
POPPLER_PATH = (
    r"C:\Users\Others\Downloads\Release-26.02.0-0"
    r"\poppler-26.02.0\Library\bin"
)

# Load TrOCR
print("Loading TrOCR Model...")
# loads microsoft TrOCR processor for handwritte text
processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-small-handwritten",
    use_fast=False
)
# loads trocr model
model = VisionEncoderDecoderModel.from_pretrained( # vision ecncoder- understands image and geneerate recognized text
    "microsoft/trocr-small-handwritten"
)

# checks whether CUDA (GPU is available)   otherwise CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# indpendent of device
model.to(device)
print("TrOCR Loaded Successfully")

# Image Preprocessing
# prepare image before sending to tesseract
def preprocess_image(image):
    image = np.array(image)    # pillow image = numpyb array
    # convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2GRAY
    )
  # gaussian blur (reduce image noise)
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )
  # thresholding(grayscale image = binary image)
    gray = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15
    )
   # back numpy array into pil image
    return Image.fromarray(gray)

# Read Typed PDF
def read_typed_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Tesseract OCR
# performs when direct text extraction doesn't give useful text
def tesseract_ocr(uploaded_file):
    images = convert_from_bytes(
        uploaded_file.read(),
        poppler_path=POPPLER_PATH
    )
    text = ""
    for image in images:
        processed = preprocess_image(image)
        page = pytesseract.image_to_string(
            processed,
            config="--oem 3 --psm 6"
        )
        text += page + "\n"
    return text

# TrOCR OCR
# for handwritten prescription
def trocr_ocr(uploaded_file):
    images = convert_from_bytes(
        uploaded_file.read(),
        poppler_path=POPPLER_PATH
    )
    text = ""
    for image in images:
        image = image.convert("RGB")
        pixel_values = processor(
            images=image,
            return_tensors="pt"
        ).pixel_values.to(device)
    # generate token IDs
        generated_ids = model.generate(
            pixel_values,
            max_length=128
        )
   # converts IDs into readable text
        generated_text = processor.batch_decode(
            generated_ids,
            skip_special_tokens=True
        )[0]
        text += generated_text + "\n"
    return text

# Smart OCR Pipeline
# decide which OCR model to use
def extract_text(uploaded_file):

    # First try typed PDF extraction
    uploaded_file.seek(0)
    text = read_typed_pdf(uploaded_file)
  # if more than 30 charctes are extracted 
    if len(text.strip()) > 30:
        print("Typed PDF Detected")
        return text

    # Then try Tesseract , if directly not extracted 
    uploaded_file.seek(0)
    text = tesseract_ocr(uploaded_file)
 # if more tha > 40 then result found 
    if len(text.strip()) > 40:
        print("Printed Prescription Detected")
        return text
    
    # Finally try TrOCR
    uploaded_file.seek(0)
    print("Handwritten Prescription Detected")
    return trocr_ocr(uploaded_file)