from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, JobSeekerProfile, RecruiterProfile

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'is_verified', 'date_joined']
    list_filter = ['user_type', 'is_verified', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_type', 'phone', 'is_verified')}),
    )

class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'experience_years', 'location', 'education']
    search_fields = ['user__username', 'user__email', 'skills']
    list_filter = ['experience_years', 'location']

class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'location']
    search_fields = ['user__username', 'user__email', 'company_name']
    list_filter = ['location']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(JobSeekerProfile, JobSeekerProfileAdmin)
admin.site.register(RecruiterProfile, RecruiterProfileAdmin)
