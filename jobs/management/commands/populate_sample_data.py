from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import CustomUser, JobSeekerProfile, RecruiterProfile
from jobs.models import Category, Job
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories = [
            'Software Development',
            'Marketing',
            'Sales',
            'Design',
            'Finance',
            'Human Resources',
            'Customer Service',
            'Engineering',
        ]
        
        for cat_name in categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'Jobs related to {cat_name}'}
            )
            if created:
                self.stdout.write(f'Created category: {cat_name}')

        # Create sample recruiter
        recruiter_user, created = CustomUser.objects.get_or_create(
            username='techcorp_hr',
            defaults={
                'email': 'hr@techcorp.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'user_type': 'recruiter',
                'is_verified': True,
            }
        )
        if created:
            recruiter_user.set_password('password123')
            recruiter_user.save()
            self.stdout.write('Created recruiter user')

        recruiter_profile, created = RecruiterProfile.objects.get_or_create(
            user=recruiter_user,
            defaults={
                'company_name': 'TechCorp Solutions',
                'company_website': 'https://techcorp.com',
                'company_description': 'Leading technology solutions company',
                'location': 'San Francisco, CA',
            }
        )

        # Create sample job seeker
        jobseeker_user, created = CustomUser.objects.get_or_create(
            username='john_developer',
            defaults={
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'user_type': 'jobseeker',
                'is_verified': True,
            }
        )
        if created:
            jobseeker_user.set_password('password123')
            jobseeker_user.save()
            self.stdout.write('Created job seeker user')

        jobseeker_profile, created = JobSeekerProfile.objects.get_or_create(
            user=jobseeker_user,
            defaults={
                'skills': 'Python, Django, JavaScript, React, SQL',
                'experience_years': 3,
                'education': 'Bachelor of Computer Science',
                'location': 'San Francisco, CA',
                'bio': 'Full-stack developer with 3 years of experience in web development.',
            }
        )

        # Create sample jobs
        software_category = Category.objects.get(name='Software Development')
        marketing_category = Category.objects.get(name='Marketing')
        
        jobs_data = [
            {
                'title': 'Senior Python Developer',
                'description': 'We are looking for an experienced Python developer to join our backend team.',
                'requirements': 'Bachelor\'s degree in Computer Science or related field\n5+ years of Python experience\nExperience with Django/Flask\nKnowledge of databases and SQL',
                'category': software_category,
                'job_type': 'full-time',
                'experience_required': '3-5',
                'salary_min': 80000,
                'salary_max': 120000,
                'location': 'San Francisco, CA',
                'skills_required': 'Python, Django, PostgreSQL, Redis, AWS',
            },
            {
                'title': 'Frontend React Developer',
                'description': 'Join our frontend team to build modern, responsive web applications.',
                'requirements': 'Bachelor\'s degree preferred\n3+ years of React experience\nExperience with TypeScript\nKnowledge of modern CSS frameworks',
                'category': software_category,
                'job_type': 'full-time',
                'experience_required': '1-3',
                'salary_min': 70000,
                'salary_max': 100000,
                'location': 'San Francisco, CA',
                'skills_required': 'React, TypeScript, HTML5, CSS3, JavaScript',
            },
            {
                'title': 'Digital Marketing Specialist',
                'description': 'Lead our digital marketing efforts across multiple channels.',
                'requirements': 'Marketing degree preferred\nGoogle Ads certification\nSocial media marketing experience\nAnalytics tools knowledge',
                'category': marketing_category,
                'job_type': 'full-time',
                'experience_required': '1-3',
                'salary_min': 50000,
                'salary_max': 75000,
                'location': 'Remote',
                'skills_required': 'Google Ads, Facebook Ads, SEO, Analytics',
            },
            {
                'title': 'Junior Software Engineer',
                'description': 'Entry-level position for new graduates interested in software development.',
                'requirements': 'Recent Computer Science graduate\nBasic programming knowledge\nEagerness to learn\nGood communication skills',
                'category': software_category,
                'job_type': 'full-time',
                'experience_required': '0-1',
                'salary_min': 60000,
                'salary_max': 80000,
                'location': 'New York, NY',
                'skills_required': 'Python, Java, Git, Basic web development',
            },
        ]

        for job_data in jobs_data:
            job, created = Job.objects.get_or_create(
                title=job_data['title'],
                recruiter=recruiter_profile,
                defaults={
                    **job_data,
                    'deadline': timezone.now() + timedelta(days=30),
                }
            )
            if created:
                self.stdout.write(f'Created job: {job_data["title"]}')

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data!'))
        self.stdout.write('Sample users created:')
        self.stdout.write('  Recruiter: techcorp_hr / password123')
        self.stdout.write('  Job Seeker: john_developer / password123')
