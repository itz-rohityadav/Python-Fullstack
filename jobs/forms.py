from django import forms
from .models import Job, JobApplication, Category

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'requirements', 'category', 'job_type',
            'experience_required', 'salary_min', 'salary_max', 'location',
            'skills_required', 'deadline'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'requirements': forms.Textarea(attrs={'rows': 6}),
            'skills_required': forms.Textarea(attrs={'rows': 3}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Write your cover letter here...'}),
        }

class JobSearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search jobs by title, company, or skills...',
            'class': 'form-control'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    job_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Job.JOB_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    experience = forms.ChoiceField(
        choices=[('', 'All Experience')] + Job.EXPERIENCE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Location...',
            'class': 'form-control'
        })
    )
