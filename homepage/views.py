from django.shortcuts import render

def homepage_index(request):
    return render(request, 'homepage_index.html')

def datasets(request):
    return render(request, 'datasets.html')

def notebooks(request):
    return render(request, 'notebooks.html')
