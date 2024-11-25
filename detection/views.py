from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth import login, authenticate, logout # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # type: ignore
from django.contrib import messages # type: ignore
from .forms import ImageUploadForm
from django.contrib.auth.models import User # type: ignore
from PIL import Image # type: ignore
import numpy as np # type: ignore
import pytesseract # type: ignore
import os
from django.contrib.auth.decorators import login_required # type: ignore
from .models import VehicleSearchHistory  # Ensure VehicleSearchHistory model exists

# Replace 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' with the actual installation path on your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Mapping for state codes
state_district_map = {
    "KA": "Karnataka",
    "MH": "Maharashtra",
    "DL": "Delhi",
    "TN": "TamilNadu",
    # Add other mappings as needed
}

def extract_state_and_district(plate_text):
    state_code = plate_text[:2].upper()
    state = state_district_map.get(state_code, "Unknown State")
    return state

# Views for rendering pages
def home_view(request):
    return render(request, 'base.html')

def contact_view(request):
    return render(request, 'detection/contact.html')

def about_view(request):
    return render(request, 'detection/about.html')

def service_view(request):
    return render(request, 'detection/service.html')

def carrers_view(request):
    return render(request, 'detection/carrers.html')

def privacy_view(request):
    return render(request, 'detection/privacy.html')

def dashboard_view(request):
    return render(request, 'detection/dashboard.html')

@login_required
def vehicle_search_history_view(request):
    search_history = VehicleSearchHistory.objects.filter(user=request.user).order_by('-search_date')
    return render(request, 'vehicle_search_history.html', {'search_history': search_history})

# Register view
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Registration successful! Please log in.")
                return redirect('login')  # Redirect to login page
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, 'detection/register.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('upload_image')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login details.")
    else:
        form = AuthenticationForm()
    return render(request, 'detection/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# Upload Image view for vehicle number plate detection
@login_required
def upload_image_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']

            try:
                img = Image.open(image)
                
                # Use pytesseract to extract text from the image
                plate_text = pytesseract.image_to_string(img, config='--psm 8')
                plate_text = plate_text.replace("\n", "").strip()  # Clean up the text

                if plate_text:
                    # Extract state from the detected text
                    state = extract_state_and_district(plate_text)
                    result = f"Detected Vehicle Number: {plate_text}, State: {state}"

                    # Save search history
                    VehicleSearchHistory.objects.create(user=request.user, image=image, result=result)
                else:
                    result = "No text detected. Please try again with a clearer image."

                return render(request, 'detection/result.html', {'prediction': result})

            except Exception as e:
                messages.error(request, f"An error occurred while processing the image: {str(e)}")
                return redirect('upload_image')
        else:
            messages.error(request, "Please upload a valid image.")
    else:
        form = ImageUploadForm()

    return render(request, 'detection/upload_image.html', {'form': form})
