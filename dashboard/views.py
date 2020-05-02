from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from dashboard.models import Dashboard, Ranking
from users.models import Profile
from dashboard.forms import CompetitionForm
from django.db.models import F
import datetime

today = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

def competition(request, pk):
    competition = Dashboard.objects.get(pk=pk)
    rankings = Ranking.objects.all()
    
    context = {
        'competition': competition,
        'rankings': rankings
    }

    return render(request, 'competition.html', context)

# Activas:
# Fecha de inicio anterior a hoy
# Fecha de finalizacion posterior a hoy
def actives(request):
    competitions = Dashboard.objects.filter(deadline__gte=today).filter(beginning__lte=today)
    
    context = {
        'competitions': competitions,
        'show_competitions': True
    }

    return render(request, 'actives.html', context)

# Proximas:
# Fecha de inicio posterior a hoy
def coming(request):
    competitions = Dashboard.objects.filter(beginning__gt=today)
    
    context = {
        'competitions': competitions,
        'show_competitions': True
    }

    return render(request, 'coming.html', context)

# Pasadas
# Fecha de finalizacion anterior a hoy
def pasts(request):
    competitions = Dashboard.objects.filter(deadline__lte=today)
    
    context = {
        'competitions': competitions,
        'show_competitions': True
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

def add_points(request, pk):

    # user = Profile.objects.filter(user=request.user)
    # user.update(points=F('points')+5)
    # if user.filter(points__gte=25): user.update(challenger=True)

    competition = Dashboard.objects.get(pk=pk)

    # ranking = Ranking.objects.filter(container=competition)

    # if ranking is None: ranking.create(container=competition)

    # ranking.update(username=request.user.username)
    # ranking.update(points=15)

    # Ranking.objects.create(container=competition,username='manu',points=10)
    
    rankings = Ranking.objects.all().order_by('-points')

    context = {
        'competition': competition,
        'rankings': rankings
    }

    return render(request, 'competition.html', context)