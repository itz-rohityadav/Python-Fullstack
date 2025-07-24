from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('jobseeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.user_type}"

# Job Seeker Profile
class JobSeekerProfile(models.Model):
    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level (0-2 years)'),
        ('mid', 'Mid Level (3-5 years)'),
        ('senior', 'Senior Level (6-10 years)'),
        ('expert', 'Expert Level (10+ years)'),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, help_text="List your skills separated by commas")
    experience_years = models.IntegerField(default=0)
    experience_level = models.CharField(max_length=10, choices=EXPERIENCE_LEVEL_CHOICES, default='entry')
    education = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True, help_text="Brief professional bio about yourself")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Additional professional fields
    job_title = models.CharField(max_length=100, blank=True, help_text="Current or desired job title")
    preferred_employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, blank=True)
    expected_salary = models.CharField(max_length=50, blank=True, help_text="Expected salary range")
    portfolio_url = models.URLField(blank=True, help_text="Link to your portfolio or personal website")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    github_url = models.URLField(blank=True, help_text="GitHub profile URL")
    
    # Availability and preferences
    availability_date = models.DateField(blank=True, null=True, help_text="When can you start?")
    willing_to_relocate = models.BooleanField(default=False, help_text="Willing to relocate for the right opportunity")
    remote_work_preference = models.BooleanField(default=False, help_text="Interested in remote work opportunities")
    
    # Professional summary
    certifications = models.TextField(blank=True, help_text="Professional certifications (one per line)")
    languages = models.CharField(max_length=200, blank=True, help_text="Languages you speak (e.g., English, Spanish)")
    
    def __str__(self):
        return f"{self.user.username} - Job Seeker"

# Recruiter Profile
class RecruiterProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_website = models.URLField(blank=True)
    company_description = models.TextField(blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.company_name}"
