from django.db import models
from django.conf import settings
from phone_field import PhoneField


User = settings.AUTH_USER_MODEL


class UserData(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_data')
    first_name = models.CharField(
        blank=False, help_text='First name', max_length=200)
    last_name = models.CharField(
        blank=False, help_text='Last name', max_length=200)
    address = models.TextField(blank=False)
    total_working_experience = models.PositiveIntegerField(
        default=0, help_text='Total working experience')
    phone_no = PhoneField(blank=True, help_text='Contact phone number')
    email = models.EmailField(
        blank=False, help_text='Email address')
    about_you = models.TextField(
        blank=False, help_text='Brief intro')
    image = models.ImageField(
        blank=False, upload_to='user', help_text='User Image')
    linkedin = models.CharField(
        blank=False, help_text='Linkedin username', max_length=200)
    facebook = models.CharField(
        blank=False, help_text='Facebook username', max_length=200)
    github = models.CharField(
        blank=False, help_text='Github username', max_length=200)
    twitter = models.CharField(
        blank=False, help_text='Twitter username', max_length=200)

    class Meta:
        verbose_name = "User data"
        verbose_name_plural = "User data"

    def __str__(self):
        return str(self.first_name)


class Experience(models.Model):
    user_experience = models.ForeignKey(
        UserData, on_delete=models.CASCADE, related_name='user_experience')
    position = models.CharField(
        blank=False, help_text='Company position', max_length=200)
    name = models.CharField(
        blank=False, help_text='Company name', max_length=200)
    joined_at = models.DateField(blank=False, null=True)
    worked_till = models.DateField(blank=False, null=True)
    description = models.TextField(blank=False, help_text='Work Description')

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experience"


class Education(models.Model):
    user_education = models.ForeignKey(
        UserData, on_delete=models.CASCADE, related_name='user_education')
    university = models.CharField(
        blank=False, help_text='University name', max_length=200)
    course = models.CharField(blank=False, help_text='Course', max_length=200)
    joined_at = models.DateField(blank=False, null=True)
    left_at = models.DateField(blank=False, null=True)
    cgpa = models.CharField(blank=False, help_text='CGPA', max_length=200)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education"


class Skills(models.Model):
    user_skills = models.ForeignKey(
        UserData, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.CharField(blank=False, help_text='skill', max_length=200)

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"


class Workflow(models.Model):
    user_workflow = models.ForeignKey(
        UserData, on_delete=models.CASCADE, related_name='user_workflow')
    workflow = models.CharField(
        blank=False, help_text='workflow', max_length=200)

    class Meta:
        verbose_name = "workflow"
        verbose_name_plural = "workflow"


class Interest(models.Model):
    user_interest = models.ForeignKey(
        UserData, on_delete=models.CASCADE, related_name='user_interest')
    interest = models.TextField(blank=False, help_text='interest')

    class Meta:
        verbose_name = "interest"
        verbose_name_plural = "interest"


class Certificate(models.Model):
    user_certificates = models.ForeignKey(
        UserData, on_delete=models.CASCADE, related_name='user_certificates')
    certificates = models.CharField(
        blank=False, help_text='certificates', max_length=200)

    class Meta:
        verbose_name = "certificates"
        verbose_name_plural = "certificates"


class Projects(models.Model):
    user_project = models.ForeignKey(
        UserData, on_delete=models.CASCADE, related_name='user_project')
    project_name = models.CharField(
        blank=False, help_text='project_name', max_length=200)
    project_description = models.TextField(
        blank=False, help_text='brief intro to project')

    class Meta:
        verbose_name = "certificates"
        verbose_name_plural = "certificates"
