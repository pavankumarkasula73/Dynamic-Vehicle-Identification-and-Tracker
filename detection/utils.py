import cv2
import numpy as np
import joblib
import pytesseract  # For OCR on the detected number plate
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

 
# Load the number plate detection model (replace with your model path)
model_path = 'detection/svm_model.pkl'
plate_model = joblib.load(model_path)
 
# Function to preprocess the uploaded image
def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((64, 64))  # Adjust the size to match the training data
    img_array = np.array(img).flatten()  # Flatten the image into a 1D array
    return img_array
 
# Detect number plate and extract text using OCR
def detect_number_plate(image: InMemoryUploadedFile):
    features, img = preprocess_image(image)
    # Predict number plate region
    plate_region = plate_model.predict(features)
    # Crop to the detected region (this part assumes `plate_region` gives bounding box coordinates)
    x, y, w, h = plate_region[0]  # Adjust this based on actual model output
    plate_img = img[y:y+h, x:x+w]
    # Perform OCR on the cropped plate region
    plate_text = pytesseract.image_to_string(plate_img, config='--psm 8')  # Adjust config if needed
    # Process the plate text to determine state and district
    state, district = extract_state_district(plate_text)
    return state, district
 
# Map number plate text to state and district
def extract_state_district(plate_text):
    # Assuming a predefined dictionary mapping plate codes to states/districts
    plate_mappings = {
        "MH": ("Maharashtra", "Mumbai"),
        "DL": ("Delhi", "Central Delhi"),
        # Add more mappings for other states and districts
    }
    # Extract state code from plate text
    state_code = plate_text[:2]
    state, district = plate_mappings.get(state_code, ("Unknown", "Unknown"))
    return state, district
 
# Example usage in a Django view
def handle_uploaded_image(image: InMemoryUploadedFile):
    state, district = detect_number_plate(image)
    if state == "Unknown":
        return "Number plate could not be classified"
    else:
        return f"Vehicle belongs to {state}, {district}"