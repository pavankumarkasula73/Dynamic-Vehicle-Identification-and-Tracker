from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload-image/', views.upload_image_view, name='upload_image'),
    path('', views.home_view, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('service/', views.service_view, name='service'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('carrers/', views.carrers_view, name='carrers'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('vehicle-search-history/', views.vehicle_search_history_view, name='vehicle_search_history')
]

