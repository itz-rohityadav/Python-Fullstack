from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import JobSeekerRegistrationForm, RecruiterRegistrationForm, JobSeekerProfileForm, RecruiterProfileForm
from .models import JobSeekerProfile, RecruiterProfile
from jobs.models import JobApplication, Job

def register_choice(request):
    return render(request, 'accounts/register_choice.html')

def jobseeker_register(request):
    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    login(request, user)
                    messages.success(request, 'Registration successful! Welcome to Job Portal.')
                    return redirect('dashboard')
            except Exception as e:
                messages.error(request, 'Registration failed. Please try again.')
    else:
        form = JobSeekerRegistrationForm()
    return render(request, 'accounts/jobseeker_register.html', {'form': form})

def recruiter_register(request):
    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    login(request, user)
                    messages.success(request, 'Registration successful! Welcome to Job Portal.')
                    return redirect('dashboard')
            except Exception as e:
                messages.error(request, 'Registration failed. Please try again.')
    else:
        form = RecruiterRegistrationForm()
    return render(request, 'accounts/recruiter_register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    context = {'user': user}
    
    if user.user_type == 'jobseeker':
        try:
            profile = user.jobseekerprofile
            applications = JobApplication.objects.filter(applicant=user)[:5]
            context.update({
                'profile': profile,
                'applications': applications,
                'total_applications': applications.count()
            })
        except JobSeekerProfile.DoesNotExist:
            JobSeekerProfile.objects.create(user=user)
            profile = user.jobseekerprofile
            context['profile'] = profile
        return render(request, 'accounts/jobseeker_dashboard.html', context)
    
    elif user.user_type == 'recruiter':
        try:
            profile = user.recruiterprofile
            jobs = Job.objects.filter(recruiter=profile)[:5]
            total_applications = JobApplication.objects.filter(job__recruiter=profile).count()
            context.update({
                'profile': profile,
                'jobs': jobs,
                'total_jobs': jobs.count(),
                'total_applications': total_applications
            })
        except RecruiterProfile.DoesNotExist:
            RecruiterProfile.objects.create(user=user, company_name='Not Set')
            profile = user.recruiterprofile
            context['profile'] = profile
        return render(request, 'accounts/recruiter_dashboard.html', context)
    
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile_edit(request):
    user = request.user
    
    if user.user_type == 'jobseeker':
        profile, created = JobSeekerProfile.objects.get_or_create(user=user)
        
        if request.method == 'POST':
            
            form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
            
            if form.is_valid():
                try:
                    saved_profile = form.save()
                    messages.success(request, f'✅ Profile updated successfully! Welcome, {user.first_name}!')
                    return redirect('dashboard')
                except Exception as e:
                    messages.error(request, f'❌ Error saving profile: {str(e)}')
            else:
                error_msgs = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_msgs.append(f"{field}: {error}")
                messages.error(request, f'❌ Please fix the following errors: {"; ".join(error_msgs)}')
        else:
            form = JobSeekerProfileForm(instance=profile)
            
        context = {
            'form': form,
            'profile': profile,
            'user': user,
            'is_jobseeker': True,
        }
        return render(request, 'accounts/jobseeker_profile_edit.html', context)
    
    elif user.user_type == 'recruiter':
        profile, created = RecruiterProfile.objects.get_or_create(
            user=user, 
            defaults={'company_name': f"{user.first_name}'s Company"}
        )
        
        if request.method == 'POST':
            
            form = RecruiterProfileForm(request.POST, request.FILES, instance=profile)
            
            if form.is_valid():
                try:
                    saved_profile = form.save()
                    messages.success(request, f'✅ Company profile updated successfully!')
                    return redirect('dashboard')
                except Exception as e:
                    messages.error(request, f'❌ Error saving profile: {str(e)}')
            else:
                error_msgs = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_msgs.append(f"{field}: {error}")
                messages.error(request, f'❌ Please fix the following errors: {"; ".join(error_msgs)}')
        else:
            form = RecruiterProfileForm(instance=profile)
            
        context = {
            'form': form,
            'profile': profile,
            'user': user,
            'is_recruiter': True,
        }
        return render(request, 'accounts/recruiter_profile_edit.html', context)
    
    messages.error(request, '❌ Invalid user type for profile editing.')
    return redirect('dashboard')

@login_required
def profile_view(request):
    user = request.user
    
    if user.user_type == 'jobseeker':
        profile, created = JobSeekerProfile.objects.get_or_create(user=user)
        return render(request, 'accounts/jobseeker_profile_view.html', {'profile': profile, 'user': user})
    
    elif user.user_type == 'recruiter':
        profile, created = RecruiterProfile.objects.get_or_create(user=user, defaults={'company_name': 'Not Set'})
        return render(request, 'accounts/recruiter_profile_view.html', {'profile': profile, 'user': user})
    
    return redirect('dashboard')
