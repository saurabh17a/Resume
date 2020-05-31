from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import NewUser
from django.contrib.auth import login, logout


def signup_view(request):
    if request.user.id is None:
        if request.method == 'POST':
            form = NewUser(request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:login_view')
        else:
            form = NewUser()
        context = {'form': form}

        return render(request, 'accounts/signup.html', context)
    else:
        return redirect('dashboard:all_resume')


def login_view(request):
    if request.user.id is None:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('dashboard:all_resume')
        else:
            form = AuthenticationForm()
        context = {'form': form}

        return render(request, 'accounts/login.html', context)
    else:
        return redirect('dashboard:all_resume')


def logout_view(request):
    if request.user.id is not None:
        logout(request)
        return redirect('accounts:login_view')
    else:
        return redirect('accounts:login_view')
