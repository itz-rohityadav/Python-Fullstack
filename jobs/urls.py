from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job-list'),
    path('<int:pk>/', views.job_detail, name='job-detail'),
    path('<int:pk>/apply/', views.job_apply, name='job-apply'),
    path('create/', views.job_create, name='job-create'),
    path('<int:pk>/edit/', views.job_edit, name='job-edit'),
    path('<int:pk>/applications/', views.job_applications, name='job-applications'),
    path('application/<int:pk>/update-status/', views.application_status_update, name='application-status-update'),
    path('my-applications/', views.my_applications, name='my-applications'),
    path('jobseeker/<int:pk>/profile/', views.recruiter_view_jobseeker_profile, name='recruiter-view-jobseeker-profile'),
    path('<int:pk>/delete/', views.job_delete, name='job-delete'),
    path('<int:pk>/toggle-status/', views.job_toggle_status, name='job-toggle-status'),
]
