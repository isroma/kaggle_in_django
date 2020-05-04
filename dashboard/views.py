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
    rankings = Ranking.objects.filter(container=competition).all().order_by('-points')
    
    context = {
        'competition': competition,
        'rankings': rankings
    }

    return render(request, 'competition.html', context)


# Active competitions:
# Beginning date before today
# Deadline date after today
# Ordered by most recent
def actives(request):
    competitions = Dashboard.objects.filter(deadline__gte=today).filter(beginning__lte=today).order_by('-beginning')
    
    context = {
        'competitions': competitions,
        'show_competitions': True
    }

    return render(request, 'actives.html', context)


# Coming competitions:
# Beginning date after today
# Ordered by closest date
def coming(request):
    competitions = Dashboard.objects.filter(beginning__gt=today).order_by('beginning')
    
    context = {
        'competitions': competitions,
        'show_competitions': True
    }

    return render(request, 'coming.html', context)


# Past competitions:
# Deadline date before today
# Ordered by last finished
def pasts(request):
    competitions = Dashboard.objects.filter(deadline__lte=today).order_by('-deadline')
    
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
    
    rankings = Ranking.objects.filter(container=competition).all().order_by('-points')

    context = {
        'competition': competition,
        'rankings': rankings
    }

    return render(request, 'competition.html', context)
    