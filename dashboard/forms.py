from django import forms
from dashboard.models import (
    UserData, Experience, Education, Skills, Workflow,
    Certificate, Projects, Interest
)


class UserDataForm(forms.ModelForm):

    class Meta:
        model = UserData
        exclude = ['user']


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        widgets = {'joined_at': forms.DateInput(attrs={'class': 'datepicker',
                                                     'type': 'date'}),
        'worked_till': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'})
        }

        exclude = ['user_experience']


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        widgets = {'joined_at': forms.DateInput(attrs={'class': 'datepicker',
                                                     'type': 'date'}),
        'left_at': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'})
        }
        exclude = ['user_education']


class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skills
        exclude = ['user_skills']


class WorkflowForm(forms.ModelForm):
    class Meta:
        model = Workflow
        exclude = ['user_workflow']


class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        exclude = ['user_interest']


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        exclude = ['user_certificates']


class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ['user_project']
