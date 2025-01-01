from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from .admin import admin_site
  # Make sure this import is correct

from . import views



urlpatterns = [
    
    path('', views.landing, name='landing'),
    path('home/', views.home_view, name='home'),
    path('accounts/login/', LoginView.as_view(template_name='detection/login.html'), name='login'),
    path('service/', views.service_view, name='service'),
    path('contact/', views.contact_view, name='contact'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),  
    
    path('logout/', views.custom_logout, name='logout'),
    path('my_account/', views.my_account, name='my_account'),
    path('upload_image/', login_required(views.upload_image_view), name='upload_image'),
    path('admin/', admin.site.urls),  
    path('accounts/', include('django.contrib.auth.urls')), 
    path('upload_video/', views.video_upload_view, name='upload_video'),
    path('upload_video_result/', views.upload_video_result, name='upload_video_result'),
    path('account/', views.account_details_view, name='account_details'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),

    
    

    
    
]