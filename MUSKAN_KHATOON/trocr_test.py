# testing file , not main appliaction file

from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

# Load TrOCR model
processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-small-handwritten"
)

model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-small-handwritten"
)

# convert pdd = image
from pdf2image import convert_from_path
images = convert_from_path(
    "sample.png.pdf",
    poppler_path=r"C:\Users\Others\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"
)
image = images[0].convert("RGB")

# Convert image for TrOCR
pixel_values = processor(
    image,
    return_tensors="pt"    # pt means PyTorch tensor is returned
).pixel_values

# Generate recognized text
generated_ids = model.generate(pixel_values)
# converts token id to normal text
text = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True
)[0]

print("\nRecognized Text:\n")
print(text)