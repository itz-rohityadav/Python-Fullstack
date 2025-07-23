from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import CustomUser, JobSeekerProfile
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Create test users Rohit and Riya with sample jobseeker profiles'

    def handle(self, *args, **options):
        # Create Rohit
        try:
            rohit = CustomUser.objects.get(username='rohit')
            self.stdout.write(self.style.WARNING('User "rohit" already exists. Updating profile...'))
        except CustomUser.DoesNotExist:
            rohit = CustomUser.objects.create_user(
                username='rohit',
                email='rohit@example.com',
                first_name='Rohit',
                last_name='Sharma',
                password='password123',
                user_type='jobseeker',
                phone='+91-9876543210'
            )
            self.stdout.write(self.style.SUCCESS('Created user "rohit"'))

        # Create or update Rohit's JobSeeker profile
        rohit_profile, created = JobSeekerProfile.objects.get_or_create(user=rohit)
        rohit_profile.job_title = 'Full Stack Developer'
        rohit_profile.skills = 'Python, Django, React, JavaScript, PostgreSQL, AWS, Docker, Git'
        rohit_profile.experience_years = 3
        rohit_profile.experience_level = 'mid'
        rohit_profile.education = 'Bachelor of Technology in Computer Science'
        rohit_profile.location = 'Mumbai, India'
        rohit_profile.bio = 'Passionate full-stack developer with 3 years of experience in building scalable web applications. Expertise in Python/Django backend development and React frontend. Love working on innovative projects that solve real-world problems.'
        rohit_profile.preferred_employment_type = 'full_time'
        rohit_profile.expected_salary = '₹8,00,000 - ₹12,00,000 per annum'
        rohit_profile.portfolio_url = 'https://rohitsharma-dev.com'
        rohit_profile.linkedin_url = 'https://linkedin.com/in/rohit-sharma-dev'
        rohit_profile.github_url = 'https://github.com/rohit-sharma-dev'
        rohit_profile.availability_date = date.today() + timedelta(days=30)
        rohit_profile.willing_to_relocate = True
        rohit_profile.remote_work_preference = True
        rohit_profile.certifications = '''AWS Certified Developer Associate
Docker Certified Associate
Scrum Master Certified'''
        rohit_profile.languages = 'English, Hindi, Marathi'
        rohit_profile.save()
        
        self.stdout.write(self.style.SUCCESS('Updated Rohit\'s jobseeker profile'))

        # Create Riya
        try:
            riya = CustomUser.objects.get(username='riya')
            self.stdout.write(self.style.WARNING('User "riya" already exists. Updating profile...'))
        except CustomUser.DoesNotExist:
            riya = CustomUser.objects.create_user(
                username='riya',
                email='riya@example.com',
                first_name='Riya',
                last_name='Patel',
                password='password123',
                user_type='jobseeker',
                phone='+91-9876543211'
            )
            self.stdout.write(self.style.SUCCESS('Created user "riya"'))

        # Create or update Riya's JobSeeker profile
        riya_profile, created = JobSeekerProfile.objects.get_or_create(user=riya)
        riya_profile.job_title = 'UI/UX Designer'
        riya_profile.skills = 'Figma, Adobe XD, Sketch, Photoshop, Illustrator, HTML, CSS, User Research, Wireframing, Prototyping'
        riya_profile.experience_years = 2
        riya_profile.experience_level = 'entry'
        riya_profile.education = 'Bachelor of Fine Arts in Graphic Design'
        riya_profile.location = 'Bangalore, India'
        riya_profile.bio = 'Creative UI/UX designer with 2 years of experience in designing user-centered digital experiences. Skilled in user research, wireframing, prototyping, and visual design. Passionate about creating intuitive and accessible designs.'
        riya_profile.preferred_employment_type = 'full_time'
        riya_profile.expected_salary = '₹5,00,000 - ₹8,00,000 per annum'
        riya_profile.portfolio_url = 'https://riyapatel-design.com'
        riya_profile.linkedin_url = 'https://linkedin.com/in/riya-patel-designer'
        riya_profile.github_url = 'https://github.com/riya-patel-design'
        riya_profile.availability_date = date.today() + timedelta(days=15)
        riya_profile.willing_to_relocate = False
        riya_profile.remote_work_preference = True
        riya_profile.certifications = '''Google UX Design Certificate
Adobe Certified Expert (ACE) - Photoshop
Figma Community Leader'''
        riya_profile.languages = 'English, Hindi, Gujarati'
        riya_profile.save()
        
        self.stdout.write(self.style.SUCCESS('Updated Riya\'s jobseeker profile'))

        self.stdout.write(
            self.style.SUCCESS('\n✅ Test users created successfully!\n')
        )
        self.stdout.write('Login credentials:')
        self.stdout.write('👤 Username: rohit | Password: password123')
        self.stdout.write('👤 Username: riya  | Password: password123')
        self.stdout.write('\n🌐 Access the application at: http://127.0.0.1:8000/')
