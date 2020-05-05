from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from dashboard.models import Dashboard, Ranking
from django.http import HttpResponse
from users.models import Profile
from dashboard.forms import CompetitionForm
from django.db.models import F
import datetime
import os


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
    form = CompetitionForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            if not request.FILES['test'].name.endswith('.csv'):
                return render(request, 'creating.html', {
                    'form': form,
                    'error_message': 'El archivo test debe tener una extensión .csv'
                })

            elif form.cleaned_data['beginning'] < today:
                error_message = 'El día de inicio no puede ser anterior a hoy (' + str(today) + ')'

                return render(request, 'creating.html', {
                    'form': form,
                    'error_message': error_message
                })

            else:
                competition = CompetitionForm()
                competition = form.save(commit=False)

                competition.test = request.FILES['test']
                competition.author = request.user.username

                competition.save()
            
                url = '/dashboard/' + str(competition.pk)

            return redirect(url)

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
    

def editing(request, pk):
    placeholder = Dashboard.objects.get(pk=pk)

    form = CompetitionForm(request.POST or None, instance=placeholder)

    context = {
        'form': form,
        'competition': placeholder,
    }

    form.fields['title'].initial = placeholder.title
    form.fields['description'].initial = placeholder.description
    form.fields['beginning'].initial = placeholder.beginning
    form.fields['deadline'].initial = placeholder.deadline
    form.fields['max_daily_uploads'].initial = placeholder.max_daily_uploads
    form.fields['wait_time_uploads'].initial = placeholder.wait_time_uploads

    if request.method == 'POST':
        if form.is_valid():
            competition = CompetitionForm()
            competition = form.save(commit=False)
            competition.save()
            
            url = '/dashboard/' + str(pk)
            return redirect(url)

    return render(request, 'editing.html', context)


def download(request, pk):
    competition = Dashboard.objects.get(pk=pk)

    response = HttpResponse(competition.train, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % competition.title

    # Creating ranking if someone participates
    user = Profile.objects.filter(user=request.user)
    user.update(points=F('points')+5)
    if user.filter(points__gte=25): user.update(challenger=True)

    # Initializing user as participant
    ranking = Ranking.objects.filter(container=competition)
    username = request.user.username
    if ranking is None: ranking.create(container=competition)
    if ranking.filter(container=competition, username=username).exists() == False: 
        ranking.create(container=competition, username=username)

    competition.participants = ranking.count()
    competition.save()

    return response