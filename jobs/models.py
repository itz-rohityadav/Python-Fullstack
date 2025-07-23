from django.db import models
from accounts.models import CustomUser, RecruiterProfile
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('0-1', '0-1 years'),
        ('1-3', '1-3 years'),
        ('3-5', '3-5 years'),
        ('5-10', '5-10 years'),
        ('10+', '10+ years'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE, related_name='jobs')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full-time')
    experience_required = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, default='0-1')
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=200)
    skills_required = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.recruiter.company_name}"
    
    @property
    def is_deadline_passed(self):
        if self.deadline:
            return timezone.now() > self.deadline
        return False

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='application_resumes/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
