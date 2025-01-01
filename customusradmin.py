# detection/customusradmin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    # Customize the admin fields, list display, etc.
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    # Add other customizations as needed.

# Unregister the default User model and register the custom version
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
