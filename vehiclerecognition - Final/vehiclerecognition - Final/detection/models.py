from django.db import models

# Create your models here.
from django.contrib.auth.models import User


"""
class UploadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)  # e.g., "Image" or "Video"
    upload_date = models.DateTimeField(auto_now_add=True)
    detected_plate_numbers = models.TextField(blank=True, null=True)  # To store multiple plate numbers
    detected_states = models.TextField(blank=True, null=True)  # To store corresponding states

    def __str__(self):
        return f"{self.user.username} - {self.file_name}"
    
        
"""

class UploadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    upload_date = models.DateTimeField(auto_now_add=True)
    detected_plate_numbers = models.TextField()  # Add this if not present
    detected_states = models.TextField()        # For state info (optional)

    def __str__(self):
        return self.file_name
    
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=32, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    

