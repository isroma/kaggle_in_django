from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as do_login, logout as do_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm

def welcome(request):
    if request.user.is_authenticated:
        return render(request, "welcome.html")

    return redirect('/login')

def register(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, "register.html", {
                    'form': form,
                    'error_message': 'Nombre de usuario ya existente'
                })

            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, "register.html", {
                    'form': form,
                    'error_message': 'Email ya utilizado previamente'
                })

            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, "register.html", {
                    'form': form,
                    'error_message': 'Las contraseñas no coinciden'
                })

            else:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )

                user.save()
               
                do_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
               
                return redirect('/users/welcome', {'user': user})

    return render(request, "register.html", {'form': form})

def login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request, user)
                return redirect('/users/welcome', {'user': user})

            elif (User.objects.filter(username=form.cleaned_data['username']).exists() == False) \
                or (User.objects.filter(username=form.cleaned_data['password']).exists() == False):
                return render(request, "login.html", {
                    'form': form,
                    'error_message': 'El usuario o la contraseña son incorrectos'
                    })

    return render(request, "login.html", {'form': form})

def logout(request):
    do_logout(request)
    return redirect('login')
