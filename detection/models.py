from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class VehicleSearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='search_history_images/')
    result = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True)
