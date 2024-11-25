from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Unregister the default User admin

from .customusradmin import CustomUserAdmin  # Import from the custom file
# Re-register with any custom configurations (or just as it is)
#admin.site.register(User, UserAdmin)

from .models import UploadHistory

@admin.register(UploadHistory)
class UploadHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_name', 'file_type', 'upload_date', 'detected_plate_numbers', 'detected_states')
    list_filter = ('file_type', 'upload_date')
    search_fields = ('user__username', 'file_name', 'detected_plate_numbers', 'detected_states')


from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile)

from django.contrib import admin

class CustomAdminSite(admin.AdminSite):
    site_header = "Custom Admin"
    site_title = "Custom Admin Portal"
    index_title = "Welcome to the Custom Admin Portal"

admin_site = CustomAdminSite(name='custom_admin')