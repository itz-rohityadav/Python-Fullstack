from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """Split a string by delimiter and return the list"""
    if not value:
        return []
    return [item.strip() for item in str(value).split(delimiter) if item.strip()]

@register.filter
def count_skills(skills_text):
    """Count the number of skills in a comma-separated string"""
    if not skills_text:
        return 0
    skills = [skill.strip() for skill in skills_text.split(',') if skill.strip()]
    return len(skills)

@register.filter
def count_certifications(cert_text):
    """Count the number of certifications in a newline-separated string"""
    if not cert_text:
        return 0
    certs = [cert.strip() for cert in cert_text.split('\n') if cert.strip()]
    return len(certs)

@register.filter
def profile_completion(profile):
    """Calculate profile completion percentage"""
    if not profile:
        return 0
    
    total_fields = 12
    completed_fields = 0
    
    # Core fields
    if profile.job_title:
        completed_fields += 1
    if profile.skills:
        completed_fields += 1
    if profile.bio:
        completed_fields += 1
    if profile.education:
        completed_fields += 1
    if profile.location:
        completed_fields += 1
    if profile.experience_years > 0:
        completed_fields += 1
    
    # Additional fields
    if profile.expected_salary:
        completed_fields += 1
    if profile.portfolio_url:
        completed_fields += 1
    if profile.linkedin_url:
        completed_fields += 1
    if profile.certifications:
        completed_fields += 1
    if profile.languages:
        completed_fields += 1
    if profile.profile_picture:
        completed_fields += 1
    
    return round((completed_fields / total_fields) * 100)
