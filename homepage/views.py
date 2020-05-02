from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import Profile

def homepage_index(request):
    return render(request, 'homepage_index.html')

def datasets(request):
    return render(request, 'datasets.html')

def notebooks(request):
    return render(request, 'notebooks.html')