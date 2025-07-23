from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_choice, name='register-choice'),
    path('register/jobseeker/', views.jobseeker_register, name='jobseeker-register'),
    path('register/recruiter/', views.recruiter_register, name='recruiter-register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.profile_edit, name='profile-edit'),
    path('profile/view/', views.profile_view, name='profile-view'),
]
