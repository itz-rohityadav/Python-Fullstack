from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.models import CustomUser, JobSeekerProfile
from .models import Job, JobApplication, Category
from .forms import JobForm, JobApplicationForm, JobSearchForm
from django.views.decorators.http import require_POST

@login_required
def job_list(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', '')
    job_type = request.GET.get('job_type', '')
    experience = request.GET.get('experience', '')
    location = request.GET.get('location', '')

    job_list = Job.objects.filter(is_active=True)

    if query:
        job_list = job_list.filter(Q(title__icontains=query) | Q(skills_required__icontains=query) | Q(recruiter__company_name__icontains=query))
    if category_id:
        job_list = job_list.filter(category_id=category_id)
    if job_type:
        job_list = job_list.filter(job_type=job_type)
    if experience:
        job_list = job_list.filter(experience_required=experience)
    if location:
        job_list = job_list.filter(location__icontains=location)

    form = JobSearchForm(request.GET)
    context = {
        'job_list': job_list,
        'form': form
    }
    return render(request, 'jobs/job_list.html', context)

@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    already_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    context = {
        'job': job,
        'apply_form': JobApplicationForm(),
        'already_applied': already_applied
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def job_apply(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('job-detail', pk=job.pk)
        else:
            messages.error(request, 'Error submitting application.')

    return redirect('job-detail', pk=job.pk)

@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user.recruiterprofile
            job.save()
            messages.success(request, 'Job created successfully!')
            return redirect('job-detail', pk=job.pk)
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('job-detail', pk=job.pk)
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {'form': form})

@require_POST
@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.recruiter.user != request.user:
        messages.error(request, 'You do not have permission to delete this job.')
        return redirect('dashboard')
    job.delete()
    messages.success(request, 'Job deleted successfully.')
    return redirect('dashboard')

@require_POST
@login_required
def job_toggle_status(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.recruiter.user != request.user:
        messages.error(request, 'You do not have permission to modify this job.')
        return redirect('dashboard')
    job.is_active = not job.is_active
    job.save()
    if job.is_active:
        messages.success(request, 'Job resumed and is now active.')
    else:
        messages.success(request, 'Job paused and is no longer visible to jobseekers.')
    return redirect('dashboard')

@login_required
def job_applications(request, pk):
    job = get_object_or_404(Job, pk=pk)
    # Ensure only the recruiter who created the job can see applications
    if job.recruiter.user != request.user:
        messages.error(request, 'You do not have permission to view these applications.')
        return redirect('job-list')
    
    applications = JobApplication.objects.filter(job=job).order_by('-applied_at')
    context = {
        'job': job,
        'applications': applications,
        'status_choices': JobApplication.STATUS_CHOICES
    }
    return render(request, 'jobs/job_applications.html', context)

@login_required
def application_status_update(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    # Ensure only the recruiter who created the job can update application status
    if application.job.recruiter.user != request.user:
        messages.error(request, 'You do not have permission to update this application.')
        return redirect('job-list')
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(JobApplication.STATUS_CHOICES):
            application.status = status
            application.save()
            messages.success(request, f'Application status updated to {application.get_status_display()}')
        else:
            messages.error(request, 'Invalid status')
    
    return redirect('job-applications', pk=application.job.pk)

@login_required
def my_applications(request):
    if request.user.user_type != 'jobseeker':
        messages.error(request, 'Only job seekers can view applications.')
        return redirect('job-list')
    
    applications = JobApplication.objects.filter(applicant=request.user).order_by('-applied_at')
    context = {'applications': applications}
    return render(request, 'jobs/my_applications.html', context)

@login_required
def recruiter_view_jobseeker_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk, user_type='jobseeker')
    profile = get_object_or_404(JobSeekerProfile, user=user)
    return render(request, 'accounts/jobseeker_profile_view.html', {'profile': profile, 'jobseeker': user})
