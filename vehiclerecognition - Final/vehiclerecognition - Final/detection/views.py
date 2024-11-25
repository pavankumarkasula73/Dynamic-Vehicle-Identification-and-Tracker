from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from .forms import CustomAuthenticationForm
from .forms import ImageUploadForm
from .forms import VideoUploadForm
from PIL import Image
import numpy as np
import pytesseract
import os
import cv2
import re
from .utils import detect_number_plates
from django.contrib.auth import views as auth_views
from .models import UploadHistory

from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .forms import ForgotPasswordForm


# Replace 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' with the actual installation path on your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load mappings of state and district codes (this should be a dictionary or function you define)
state_district_map = {
    'AP': 'Andhra Pradesh',
    'AR': 'Arunachal Pradesh',
    'AS': 'Assam',
    'BR': 'Bihar',
    'CG': 'Chhattisgarh',
    'GA': 'Goa',
    'GJ': 'Gujarat',
    'HR': 'Haryana',
    'HP': 'Himachal Pradesh',
    'JH': 'Jharkhand',
    'KA': 'Karnataka',
    'KL': 'Kerala',
    'MP': 'Madhya Pradesh',
    'MH': 'Maharashtra',
    'MN': 'Manipur',
    'ML': 'Meghalaya',
    'MZ': 'Mizoram',
    'NL': 'Nagaland',
    'OR': 'Odisha',
    'PB': 'Punjab',
    'RJ': 'Rajasthan',
    'SK': 'Sikkim',
    'TN': 'Tamil Nadu',
    'TS': 'Telangana',
    'TR': 'Tripura',
    'UP': 'Uttar Pradesh',
    'UK': 'Uttarakhand',
    'WB': 'West Bengal',
    'AN': 'Andaman and Nicobar Islands',
    'CH': 'Chandigarh',
    'DN': 'Dadra and Nagar Haveli and Daman and Diu',
    'DL': 'Delhi',
    'JK': 'Jammu and Kashmir',
    'LA': 'Ladakh',
    'LD': 'Lakshadweep',
    'PY': 'Puducherry'
    # Add other mappings as needed
}

# Function to extract state and district from the vehicle number
def extract_state_and_district(plate_text):
    # Extract the first two characters to identify the state
    state_code = plate_text[:2].upper()
    state = state_district_map.get(state_code, "Unknown State")
    # Add custom logic here if you want to extract district codes or other details from the plate text
    return state


#landing
def landing(request):
    # Renders the base.html template as the landing page
    return render(request, 'base.html')

# Home view
@login_required(login_url='/login/') 
def home_view(request):
    return render(request, 'home.html')

# Service view
@login_required(login_url='/login/')
def service_view(request):
    
    return render(request, 'service.html')

# Contact View
@login_required(login_url='/login/')
def contact_view(request):
    return render(request, 'contact.html')

"""
# Register view
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('login')

    return render(request, 'detection/register.html')

"""



# Register View
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        # Create and save the user
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('login')

    return render(request, 'detection/register.html')

# Login view


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            # Check if the input is an email or username
            if '@' in username_or_email:
                try:
                    user = User.objects.get(email=username_or_email)
                    username = user.username
                except User.DoesNotExist:
                    username = None
            else:
                username = username_or_email

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('home')
            else:
                messages.error(request, "Invalid login credentials.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'detection/login.html', {'form': form})




# Logout view
"""
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')
"""

# Logout View
"""
def logout_view(request):
    logout(request)
    return redirect('login')  
"""

#Custom logout
def custom_logout(request):
    logout(request)
    return redirect('login')



# My Account View
def my_account(request):
    return render(request, 'my_account.html')

# Upload Image view for vehicle number plate detection
@login_required(login_url='/login/')
def upload_image_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']

            try:
                img = Image.open(image)
                plate_text = pytesseract.image_to_string(img, config='--psm 8').replace("\n", "").strip()
                state = extract_state_and_district(plate_text) if plate_text else "Unknown"

                # Save to UploadHistory
                UploadHistory.objects.create(
                    user=request.user,
                    file_name=image.name,
                    file_type="Image",
                    detected_plate_numbers=plate_text,
                    detected_states=state,
                )

                result = f"Detected Vehicle Number: {plate_text}\nState: {state}" if plate_text else "No text detected."
                return render(request, 'detection/result.html', {'prediction': result})

            except Exception as e:
                messages.error(request, f"An error occurred while processing the image: {str(e)}")
                return redirect('upload_image')
    else:
        form = ImageUploadForm()
    return render(request, 'detection/upload_image.html', {'form': form})
# Extract state based on vehicle number prefix
def extract_state(plate_text):
    state_code = plate_text[:2].upper()
    return state_district_map.get(state_code, "Unknown State")

# Number plate detection function
def number_plate_detection(img):
    def clean2_plate(plate):
        gray_img = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_img, 110, 255, cv2.THRESH_BINARY)
        num_contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if num_contours:
            contour_area = [cv2.contourArea(c) for c in num_contours]
            max_cntr_index = np.argmax(contour_area)
            max_cnt = num_contours[max_cntr_index]
            x, y, w, h = cv2.boundingRect(max_cnt)

            if not ratio_check(contour_area[max_cntr_index], w, h):
                return plate, None

            final_img = thresh[y:y + h, x:x + w]
            return final_img, [x, y, w, h]
        else:
            return plate, None

    def ratio_check(area, width, height):
        ratio = float(width) / float(height) if height > 0 else 0
        if area < 1063.62 or area > 73862.5 or ratio < 3 or ratio > 6:
            return False
        return True

    img2 = cv2.GaussianBlur(img, (5, 5), 0)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2 = cv2.Sobel(img2, cv2.CV_8U, 1, 0, ksize=3)
    _, img2 = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(17, 3))
    morph_img_threshold = cv2.morphologyEx(img2, cv2.MORPH_CLOSE, kernel=element)
    num_contours, _ = cv2.findContours(morph_img_threshold, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

    for cnt in num_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        plate_img = img[y:y + h, x:x + w]
        clean_plate, rect = clean2_plate(plate_img)
        if rect:
            plate_im = Image.fromarray(clean_plate)
            text = pytesseract.image_to_string(plate_im, lang='eng')
            return "".join(re.split("[^a-zA-Z0-9]*", text)).upper()
    return ""

# View to upload video for processing
@login_required(login_url='/login/')
def video_upload_view(request):
    if request.method == 'POST' and request.FILES['video']:
        video_file = request.FILES['video']
        fs = FileSystemStorage()
        filename = fs.save(video_file.name, video_file)
        video_path = os.path.join('media', filename)

        cap = cv2.VideoCapture(video_path)
        detected_numbers = set()
        detected_states = set()
        frame_counter = 0
        frame_interval = 30

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            plate_text = number_plate_detection(frame)
            if plate_text and frame_counter % frame_interval == 0:
                detected_numbers.add(plate_text)
                detected_states.add(extract_state_and_district(plate_text))

            frame_counter += 1

        cap.release()

        # Save to UploadHistory
        UploadHistory.objects.create(
            user=request.user,
            file_name=video_file.name,
            file_type="Video",
            detected_plate_numbers=", ".join(detected_numbers),
            detected_states=", ".join(detected_states),
        )

        request.session['detected_numbers'] = list(detected_numbers)
        return redirect('upload_video_result')

    return render(request, 'detection/upload_video.html')

def normalize_plate_text(plate_text):
    """Normalize the plate text to handle minor variations in OCR results."""
    # Remove any unwanted characters, extra spaces, and make the text uppercase
    normalized_text = ''.join(re.split(r'\W+', plate_text)).upper()  # Only keep alphanumeric characters
    return normalized_text.strip()

# Display detected results from video
@login_required(login_url='/login/')
def upload_video_result(request):
    detected_numbers = request.session.get('detected_numbers', [])
    vehicle_data = [
        (number, state_district_map.get(number[:2].upper(), "Unknown State"))
        for number in detected_numbers
    ]
    return render(request, 'detection/upload_video_result.html', {'vehicle_data': vehicle_data})


@login_required(login_url='/login/')
def account_details_view(request):
    user = request.user
    upload_history = UploadHistory.objects.filter(user=user).order_by('-upload_date')
    return render(request, 'detection/account_details.html', {
        'user': user,
        'upload_history': upload_history
    })

    

# Forgot Password View
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)

            # Generate a password reset token
            token = get_random_string(length=32)
            # Save token to the user for later verification (this example is simplified)
            user.profile.reset_token = token  # Assuming you've added this field to the user profile model
            user.profile.save()

            # Send password reset email
            reset_link = f'http://127.0.0.1:8000/reset-password/{token}/'
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'admin@vehiclerecognition.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'A password reset link has been sent to your email.')
            return redirect('forgot_password')
    else:
        form = ForgotPasswordForm()

    return render(request, 'detection/forgot_password.html', {'form': form})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Step 1: Check if email exists
        if not request.POST.get('new_password') and not request.POST.get('confirm_password'):
            try:
                user = User.objects.get(email=email)
                # If email exists, show password fields
                return render(request, 'detection/forgot_password.html', {
                    'email_entered': True,
                    'email': email
                })
            except User.DoesNotExist:
                # If email doesn't exist, show error message
                messages.error(request, "Invalid Email ID.")
                return render(request, 'detection/forgot_password.html')

        # Step 2: Reset password if new password is provided
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password has been reset successfully. You can now log in with the new password.")
            return redirect('login')  # Redirect to login page after password reset
        else:
            messages.error(request, "Passwords do not match. Please try again.")
            return render(request, 'detection/forgot_password.html', {
                'email_entered': True,
                'email': email
            })

    return render(request, 'detection/forgot_password.html', {
        'email_entered': False
    })


