from django.shortcuts import render, redirect, get_object_or_404
from dashboard.forms import (
    UserDataForm, ExperienceForm, EducationForm,
    SkillsForm, WorkflowForm, ProjectsForm, CertificateForm, InterestForm
)
from django.views import View
from django.http import HttpResponse

from dashboard.models import (
    UserData, Experience, Education,
    Skills, Workflow, Projects, Certificate, Interest
)
from accounts.models import Profile as User
from django.contrib.auth.decorators import login_required
from dashboard.utils import render_to_pdf
import requests
import json
import os


def user_resume(request, id):
    data = UserData.objects.get(id=id)
    experience = Experience.objects.filter(user_experience=data).all().order_by('-worked_till')
    education = Education.objects.filter(user_education=data).all().order_by('-left_at')
    skills = Skills.objects.filter(user_skills=data).all()
    workflow = Workflow.objects.filter(user_workflow=data).all()
    interest = Interest.objects.filter(user_interest=data).all()
    award = Certificate.objects.filter(user_certificates=data).all()
    project = Projects.objects.filter(user_project=data).all()
    context = {'data': data, 'award': award, 'project': project, 'experience': experience,'interest':interest, 'education': education, 'skills':skills, 'workflow':workflow}
    return render(request, 'dashboard/view_resume.html', context=context)


@login_required(login_url="/accounts/login/")
def create_info(request):
    if request.user.user_types == 'Candidate':
        if request.method == 'POST':
            add_user_data = UserDataForm(request.POST, request.FILES)
            if add_user_data.is_valid():
                user_data = add_user_data.save(commit=False)
                user_data.user = request.user
                user_data.save()
                user_data_id = user_data.id
                return redirect('dashboard:add_details', id=user_data_id)
        else:
            add_user_data = UserDataForm()
        context = {'add_user_data': add_user_data}
        return render(request, 'dashboard/info.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def add_details(request, id):
    user_data = UserData.objects.get(id=id)

    experiences = Experience.objects.filter(user_experience=user_data).all()
    if request.user == user_data.user:
        user_data_id = user_data.id
        context = {'user_data_id': user_data_id, 'user_data': user_data, 'experiences': experiences}
        return render(request, 'dashboard/add_details.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def update_details(request, id=None):
    obj_details = get_object_or_404(UserData, id=id)
    if obj_details.user == request.user:
        add_user_details = UserDataForm(
            request.POST or None, request.FILES or None, instance=obj_details)

        user_data = obj_details.user

        if request.method == 'POST':
            if add_user_details.is_valid():
                user_exp = add_user_details.save(commit=False)
                user_exp.user = user_data
                if request.FILES.get('image'):
                    user_exp.image = request.FILES.get('image')
                else:
                    user_exp.image = obj_details.image
                user_exp.save()
                return redirect('dashboard:all_resume')

        context = {'add_user_details': add_user_details, 'user_data': obj_details}
        return render(request, 'dashboard/details_update.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def all_resume(request):
    if request.user.user_types == 'Candidate':
        user_data = UserData.objects.filter(user=request.user).all()
        context = {'user_data': user_data}
        return render(request, 'dashboard/all_resume.html', context=context)
    else:
        user_data = UserData.objects.all()
        context = {'user_data': user_data}
        return render(request, 'dashboard/all_resumes.html', context=context)

@login_required(login_url="/accounts/login/")
def search_resume(request):
    if request.user.user_types == 'Recruiter':
        if request.method == 'POST':
            exp = request.POST.get('exp')
            skill = request.POST.get('skill')
            users_skill = Skills.objects.filter(skill__icontains=skill).all()
            skills_data = []
            for skl in users_skill:
                skills_data.append(skl.user_skills)
            user_data = []
            for user_skill_data in skills_data:
                if user_skill_data.total_working_experience >= int(exp):
                    user_data.append(user_skill_data)
            context = {'user_data': user_data}
            return render(request, 'dashboard/all_resumes.html', context=context)
        else:
            return render(request, 'dashboard/search.html')
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def delete_resume(request, id=None):
    resume = UserData.objects.get(id=id)
    if request.user == resume.user:
        resume.delete()
        return redirect('dashboard:all_resume')
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def create_experience(request, id):
    user_data = UserData.objects.get(id=id)
    if request.user == user_data.user:
        if request.method == 'POST':
            add_user_experience = ExperienceForm(request.POST)
            if add_user_experience.is_valid():
                user_exp = add_user_experience.save(commit=False)
                user_exp.user_experience = user_data
                user_exp.save()
                return redirect('dashboard:add_details', id=user_data.id)
        else:
            add_user_experience = ExperienceForm()
        context = {'add_user_experience': add_user_experience, "user_data": user_data}
        return render(request, 'dashboard/experience.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def list_experience(request, id):
    user_data = UserData.objects.get(id=id)
    if user_data.user == request.user:
        experiences = Experience.objects.filter(user_experience=user_data).all()
        return render(
            request, 'dashboard/experience_list.html',
            {'experiences': experiences, 'user_data': user_data})
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def update_experience(request, id=None):
    obj_experience = get_object_or_404(Experience, id=id)
    if obj_experience.user_experience.user == request.user:
        add_user_experience = ExperienceForm(
            request.POST or None, instance=obj_experience)

        user_data = obj_experience.user_experience

        if request.method == 'POST':
            if add_user_experience.is_valid():
                user_exp = add_user_experience.save(commit=False)
                user_exp.user_experience = user_data
                user_exp.save()
                return redirect('dashboard:list_experience', id=user_data.id)

        context = {'add_user_experience': add_user_experience, 'user_data': user_data}
        return render(request, 'dashboard/experience_update.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def delete_experience(request, id=None):
    experience = Experience.objects.get(id=id)
    if experience.user_experience.user == request.user:
        user_data_id = experience.user_experience.id
        experience.delete()
        return redirect('dashboard:list_experience', id=user_data_id)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def create_education(request, id):
    user_data = UserData.objects.get(id=id)
    if request.user == user_data.user:
        if request.method == 'POST':
            add_user_education = EducationForm(request.POST)
            if add_user_education.is_valid():
                user_edu = add_user_education.save(commit=False)
                user_edu.user_education = user_data
                user_edu.save()
                return redirect('dashboard:add_details', id=user_data.id)
        else:
            add_user_education = EducationForm()
        context = {'add_user_education': add_user_education, 'user_data': user_data}
        return render(request, 'dashboard/education.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def list_education(request, id):
    user_data = UserData.objects.get(id=id)
    if user_data.user == request.user:
        educations = Education.objects.filter(user_education=user_data).all()
        return render(
            request, 'dashboard/education_list.html',
            {'educations': educations, "user_data": user_data})
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def update_education(request, id=None):
    obj_education = get_object_or_404(Education, id=id)
    if obj_education.user_education.user == request.user:
        add_user_education = EducationForm(
            request.POST or None, instance=obj_education)

        user_data = obj_education.user_education

        if request.method == 'POST':
            if add_user_education.is_valid():
                user_exp = add_user_education.save(commit=False)
                user_exp.user_education = user_data
                user_exp.save()
                return redirect('dashboard:list_education', id=user_data.id)

        context = {'add_user_education': add_user_education, 'user_data': user_data}
        return render(request, 'dashboard/education_update.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def delete_education(request, id=None):
    education = Education.objects.get(id=id)
    if education.user_education.user == request.user:
        user_data_id = education.user_education.id
        education.delete()
        return redirect('dashboard:list_education', id=user_data_id)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def create_skills(request, id):
    user_data = UserData.objects.get(id=id)
    if user_data.user == request.user:
        if request.method == 'POST':
            add_user_skills = SkillsForm(request.POST)
            if add_user_skills.is_valid():
                user_skill = add_user_skills.save(commit=False)
                user_skill.user_skills = user_data
                user_skill.save()
                if 'Python' or 'python' in user_skill.skill:
                    webhook = os.environ.get("webhook_slack")
                    data = {"text": "http://127.0.0.1:8000/viewresume/{}".format(id)}
                    requests.post(webhook, json.dumps(data))
                return redirect('dashboard:add_details', id=user_data.id)
        else:
            add_user_skills = SkillsForm()
        context = {'add_user_skills': add_user_skills, 'user_data': user_data}
        return render(request, 'dashboard/skills.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def list_skill(request, id):
    user_data = UserData.objects.get(id=id)
    if user_data.user == request.user:
        skills = Skills.objects.filter(user_skills=user_data).all()
        return render(
            request, 'dashboard/skill_list.html',
            {'skills': skills, 'user_data': user_data})
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def update_skill(request, id=None):
    obj_skill = get_object_or_404(Skills, id=id)
    if obj_skill.user_skills.user == request.user:
        add_user_skill = SkillsForm(
            request.POST or None, instance=obj_skill)

        user_data = obj_skill.user_skills

        if request.method == 'POST':
            if add_user_skill.is_valid():
                user_exp = add_user_skill.save(commit=False)
                user_exp.user_skills = user_data
                user_exp.save()
                return redirect('dashboard:list_skill', id=user_data.id)

        context = {'add_user_skill': add_user_skill, 'user_data': user_data}
        return render(request, 'dashboard/skill_update.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def delete_skill(request, id=None):
    skill = Skills.objects.get(id=id)
    if skill.user_skills.user == request.user:
        user_data_id = skill.user_skills.id
        skill.delete()
        return redirect('dashboard:list_skill', id=user_data_id)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def create_workflow(request, id):
    user_data = UserData.objects.get(id=id)
    if request.user == user_data.user:
        if request.method == 'POST':
            add_user_workflow = WorkflowForm(request.POST)
            if add_user_workflow.is_valid():
                user_workflows = add_user_workflow.save(commit=False)
                user_workflows.user_workflow = user_data
                user_workflows.save()
                return redirect('dashboard:add_details', id=user_data.id)
        else:
            add_user_workflow = WorkflowForm()
        context = {'add_user_workflow': add_user_workflow, 'user_data': user_data}
        return render(request, 'dashboard/workflow.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def list_workflow(request, id):
    user_data = UserData.objects.get(id=id)
    if request.user ==  user_data.user:
        workflows = Workflow.objects.filter(user_workflow=user_data).all()
        return render(
            request, 'dashboard/workflow_list.html',
            {'workflows': workflows, 'user_data': user_data})
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def update_workflow(request, id=None):
    obj_workflow = get_object_or_404(Workflow, id=id)
    if obj_workflow.user_workflow.user == request.user:
        add_user_workflow = WorkflowForm(
            request.POST or None, instance=obj_workflow)

        user_data = obj_workflow.user_workflow

        if request.method == 'POST':
            if add_user_workflow.is_valid():
                user_exp = add_user_workflow.save(commit=False)
                user_exp.user_workflow = user_data
                user_exp.save()
                return redirect('dashboard:list_workflow', id=user_data.id)

        context = {'add_user_workflow': add_user_workflow, 'user_data': user_data}
        return render(request, 'dashboard/workflow_update.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def delete_workflow(request, id=None):
    workflow = Workflow.objects.get(id=id)
    if workflow.user_workflow.user == request.user:
        user_data_id = workflow.user_workflow.id
        workflow.delete()
        return redirect('dashboard:list_workflow', id=user_data_id)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def create_certificates(request, id):
    user_data = UserData.objects.get(id=id)
    if user_data.user == request.user:
        if request.method == 'POST':
            add_user_certificates = CertificateForm(request.POST)
            if add_user_certificates.is_valid():
                user_certificate = add_user_certificates.save(commit=False)
                user_certificate.user_certificates = user_data
                user_certificate.save()
                return redirect('dashboard:add_details', id=user_data.id)
        else:
            add_user_certificates = CertificateForm()
        context = {'add_user_certificates': add_user_certificates, 'user_data': user_data}
        return render(request, 'dashboard/certificates.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def list_certificate(request, id):
    user_data = UserData.objects.get(id=id)
    if user_data.user == request.user:
        certificates = Certificate.objects.filter(user_certificates=user_data).all()
        return render(
            request, 'dashboard/certificate_list.html',
            {'certificates': certificates, 'user_data': user_data})
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def update_certificate(request, id=None):
    obj_certificate = get_object_or_404(Certificate, id=id)
    if obj_certificate.user_certificates.user == request.user:
        add_user_certificate = CertificateForm(
            request.POST or None, instance=obj_certificate)

        user_data = obj_certificate.user_certificates

        if request.method == 'POST':
            if add_user_certificate.is_valid():
                user_exp = add_user_certificate.save(commit=False)
                user_exp.user_certificates = user_data
                user_exp.save()
                return redirect('dashboard:list_certificate', id=user_data.id)

        context = {'add_user_certificate': add_user_certificate, 'user_data': user_data}
        return render(request, 'dashboard/certificate_update.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def delete_certificate(request, id=None):
    certificate = Certificate.objects.get(id=id)
    if certificate.user_certificates.user == request.user:
        user_data_id = certificate.user_certificates.id
        certificate.delete()
        return redirect('dashboard:list_certificate', id=user_data_id)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def create_projects(request, id):
    user_data = UserData.objects.get(id=id)
    if user_data.user == request.user:
        if request.method == 'POST':
            add_user_projects = ProjectsForm(request.POST)
            if add_user_projects.is_valid():
                user_projects = add_user_projects.save(commit=False)
                user_projects.user_project = user_data
                user_projects.save()
                return redirect('dashboard:add_details', id=user_data.id)
        else:
            add_user_projects = ProjectsForm()
        context = {'add_user_projects': add_user_projects, 'user_data': user_data}
        return render(request, 'dashboard/projects.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def list_project(request, id):
    user_data = UserData.objects.get(id=id)
    if user_data.user == request.user:
        projects = Projects.objects.filter(user_project=user_data).all()
        return render(
            request, 'dashboard/project_list.html',
            {'projects': projects, 'user_data': user_data})
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def update_project(request, id=None):
    obj_project = get_object_or_404(Projects, id=id)
    if obj_project.user_project.user == request.user:
        add_user_project = ProjectsForm(
            request.POST or None, instance=obj_project)

        user_data = obj_project.user_project

        if request.method == 'POST':
            if add_user_project.is_valid():
                user_exp = add_user_project.save(commit=False)
                user_exp.user_project = user_data
                user_exp.save()
                return redirect('dashboard:list_project', id=user_data.id)

        context = {'add_user_project': add_user_project, 'user_data': user_data}
        return render(request, 'dashboard/project_update.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def delete_project(request, id=None):
    project = Projects.objects.get(id=id)
    if project.user_project.user == request.user:
        user_data_id = project.user_projects.id
        project.delete()
        return redirect('dashboard:list_project', id=user_data_id)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def create_interests(request, id):
    user_data = UserData.objects.get(id=id)
    if user_data.user == request.user:
        if request.method == 'POST':
            add_user_interests = InterestForm(request.POST)
            if add_user_interests.is_valid():
                user_interests = add_user_interests.save(commit=False)
                user_interests.user_interest = user_data
                user_interests.save()
                return redirect('dashboard:add_details', id=user_data.id)
        else:
            add_user_interests = InterestForm()
        context = {'add_user_interests': add_user_interests, 'user_data': user_data}
        return render(request, 'dashboard/interests.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def list_interest(request, id):
    user_data = UserData.objects.get(id=id)
    if user_data.user == request.user:
        interests = Interest.objects.filter(user_interest=user_data).all()
        return render(
            request, 'dashboard/interest_list.html',
            {'interests': interests, 'user_data': user_data})
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def update_interest(request, id=None):
    obj_interest = get_object_or_404(Interest, id=id)
    if obj_interest.user_interest.user == request.user:
        add_user_interest = InterestForm(
            request.POST or None, instance=obj_interest)

        user_data = obj_interest.user_interest

        if request.method == 'POST':
            if add_user_interest.is_valid():
                user_exp = add_user_interest.save(commit=False)
                user_exp.user_interest = user_data
                user_exp.save()
                return redirect('dashboard:list_interest', id=user_data.id)

        context = {'add_user_interest': add_user_interest, 'user_data': user_data}
        return render(request, 'dashboard/interest_update.html', context=context)
    else:
        return redirect('dashboard:all_resume')


@login_required(login_url="/accounts/login/")
def delete_interest(request, id=None):
    interest = Interest.objects.get(id=id)
    if interest.user_interest.user == request.user:
        user_data_id = interest.user_interest.id
        interest.delete()
        return redirect('dashboard:list_interest', id=user_data_id)
    else:
        return redirect('dashboard:all_resume')


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        data = UserData.objects.get(id=self.kwargs['id'])
        experience = Experience.objects.filter(user_experience=data).all().order_by('-worked_till')
        education = Education.objects.filter(user_education=data).all().order_by('-left_at')
        skills = Skills.objects.filter(user_skills=data).all()
        workflow = Workflow.objects.filter(user_workflow=data).all()
        interest = Interest.objects.filter(user_interest=data).all()
        award = Certificate.objects.filter(user_certificates=data).all()
        project = Projects.objects.filter(user_project=data).all()
        context = {'data': data, 'award': award, 'project': project, 'experience': experience,'interest':interest, 'education': education, 'skills':skills, 'workflow':workflow}
        pdf = render_to_pdf('dashboard/resume.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


def error_404_view(request, exception):
    templates = 'dashboard/404.html'
    return render(request, templates)


def error_500_view(request, *args, **argv):
    templates = 'dashboard/500.html'
    return render(request, templates)
