from django.shortcuts import render, redirect
from dashboard.models import Dashboard
from dashboard.forms import CompetitionForm
import datetime

today = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

def competition(request, pk):
    competition = Dashboard.objects.get(pk=pk)
    show_competitions = True
    context = {
        'competition': competition,
        'show_competitions': show_competitions
    }
    print("hola")
    return render(request, 'competition.html', context)

# Activas:
# Fecha de inicio anterior a hoy
# Fecha de finalizacion posterior a hoy
def actives(request):
    competitions = Dashboard.objects.filter(deadline__gte=today).filter(beginning__lte=today)
    context = {
        'competitions': competitions
    }
    return render(request, 'actives.html', context)

# Proximas:
# Fecha de inicio posterior a hoy
def coming(request):
    competitions = Dashboard.objects.filter(beginning__gt=today)
    context = {
        'competitions': competitions
    }
    return render(request, 'coming.html', context)

# Pasadas
# Fecha de finalizacion anterior a hoy
def pasts(request):
    competitions = Dashboard.objects.filter(deadline__lte=today)
    context = {
        'competitions': competitions
    }
    return render(request, 'pasts.html', context)

def creating(request):
    form = CompetitionForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            competition = CompetitionForm()
            competition = form.save(commit=False)
            
            competition.participants = 0
            competition.author = request.user.username
            competition.save()
            
            return redirect('/dashboard/actives')

    return render(request, 'creating.html', {'form': form})

def delete(request, pk):
    competition = Dashboard.objects.get(pk=pk)
    competition.delete()
    return redirect('/dashboard/actives')
