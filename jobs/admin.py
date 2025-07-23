from django.contrib import admin
from .models import Category, Job, JobApplication

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'recruiter', 'category', 'job_type', 'location', 'is_active', 'created_at']
    list_filter = ['job_type', 'category', 'is_active', 'experience_required']
    search_fields = ['title', 'recruiter__company_name', 'location']
    date_hierarchy = 'created_at'

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['applicant__username', 'job__title']
    date_hierarchy = 'applied_at'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
