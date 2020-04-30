from django.shortcuts import render
from django.contrib.auth.models import User

def homepage_index(request):
    return render(request, 'homepage_index.html')
