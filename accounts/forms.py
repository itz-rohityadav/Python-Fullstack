from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, JobSeekerProfile, RecruiterProfile

class JobSeekerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.user_type = 'jobseeker'
        if commit:
            user.save()
            JobSeekerProfile.objects.create(user=user)
        return user

class RecruiterRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=False)
    company_name = forms.CharField(max_length=200, required=True)
    company_website = forms.URLField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.user_type = 'recruiter'
        if commit:
            user.save()
            RecruiterProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                company_website=self.cleaned_data['company_website']
            )
        return user

class JobSeekerProfileForm(forms.ModelForm):
    availability_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = JobSeekerProfile
        fields = [
            'profile_picture', 'job_title', 'skills', 'experience_years', 'experience_level',
            'education', 'location', 'bio', 'preferred_employment_type', 'expected_salary',
            'portfolio_url', 'linkedin_url', 'github_url', 'availability_date',
            'willing_to_relocate', 'remote_work_preference', 'certifications',
            'languages', 'resume'
        ]
        widgets = {
            'skills': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'List your skills (e.g., Python, JavaScript, Project Management)'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Write a brief professional bio about yourself'
            }),
            'certifications': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'List your certifications (one per line)'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '50'
            }),
            'experience_level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'preferred_employment_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'education': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your highest education qualification'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your location'
            }),
            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Current or desired job title'
            }),
            'expected_salary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Expected salary range (e.g., $50,000 - $70,000)'
            }),
            'portfolio_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourportfolio.com'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/yourprofile'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/yourusername'
            }),
            'languages': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Languages you speak (e.g., English, Spanish, French)'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'willing_to_relocate': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'remote_work_preference': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['company_name', 'company_website', 'company_description', 'company_logo', 'location']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name',
                'required': True
            }),
            'company_website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.example.com'
            }),
            'company_description': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Describe your company, its mission, and what makes it unique'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company location'
            }),
            'company_logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
