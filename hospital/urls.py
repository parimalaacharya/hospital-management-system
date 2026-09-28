from django.urls import path
from . import views
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import PatientForm
from .models import Patient

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register_patient, name='register_patient'),
    path('patients/', views.patient_list, name='patient_list'),
    path('edit/<int:id>/', views.edit_patient, name='edit_patient'),
    path('delete/<int:id>/', views.delete_patient, name='delete_patient'),
    path('patient/<int:id>/', views.patient_detail, name='patient_detail'),
]