from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from dashboard.models import Dashboard, Ranking
from django.http import HttpResponse
from users.models import Profile
from dashboard.forms import CompetitionForm, SubmissionForm
from django.db.models import F
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from sklearn.metrics import roc_auc_score
import pandas as pd
import datetime
import os


today = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)


def competition(request, pk):
    competition = Dashboard.objects.get(pk=pk)
    rankings = Ranking.objects.filter(container=competition).all().order_by('-points')
    
    form = SubmissionForm(request.POST or None, request.FILES or None)
    ranking = Ranking.objects.filter(container=competition,username=request.user.username)

    if request.method == 'POST':
        if form.is_valid():
            if not request.FILES['submission'].name.endswith('.csv'):
                return render(request, 'competition.html', {
                    'competition': competition,
                    'rankings': rankings,
                    'form': form,
                    'error_message': 'El archivo debe tener una extensión .csv'
                })

            elif ranking.exists() == False:
                return render(request, 'competition.html', {
                    'competition': competition,
                    'rankings': rankings,
                    'form': form,
                    'error_message': 'Primero tienes que descargarte el .py para poder subir un archivo'
                })

            else:
                submission = SubmissionForm()
                submission = form.save(commit=False)
                submission.container_id = pk

                ranking.update(submission=request.FILES['submission'])
                
                submission.save()

                if Ranking.objects.filter(container=competition, username='').exists(): Ranking.objects.filter(container=competition, username='').delete()

                df_private = pd.read_csv(competition.private)
                df_private.columns = ['id','real']
                df_private.index = df_private.id
                df_submission = pd.read_csv(Ranking.objects.get(container=competition, username=request.user.username).submission)
                df_merged = pd.merge(df_private, df_submission, left_index=True, right_index=True, how='left')
                df_merged.fillna(0, inplace=True)

                ranking.update(points=(2*roc_auc_score(df_merged.real, df_merged.pred)-1))

    context = {
        'competition': competition,
        'rankings': rankings,
        'form': form
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

                temp_test = request.FILES['test']
                temp_test = pd.read_csv(temp_test)
                competition.private = ContentFile(temp_test.copy().drop(columns=temp_test.columns[0:-1]).to_csv())
                competition.private.name = competition.title + '_private.csv'
                competition.test = ContentFile(temp_test.iloc[:,:-1].to_csv())
                competition.test.name = competition.title + '_test.csv'

                competition.train = request.FILES['train']
                competition.train.name = competition.title + '_train.csv'

                competition.author = request.user.username

                competition.save()
            
                url = '/dashboard/' + str(competition.pk)

            return redirect(url)

    return render(request, 'creating.html', {'form': form})


def delete(request, pk):
    competition = Dashboard.objects.get(pk=pk)
    competition.delete()
    return redirect('/dashboard/actives')


# For testing
def add_points(request, pk):

    # user = Profile.objects.filter(user=request.user)
    # user.update(points=F('points')+5)
    # if user.filter(points__gte=25): user.update(challenger=True)

    competition = Dashboard.objects.get(pk=pk)

    ranking = Ranking.objects.get(container=competition, username=request.user.username)

    print(ranking.container_id)

    # if ranking is None: ranking.create(container=competition)

    # ranking.update(username=request.user.username)
    # ranking.update(points=15)

    # Ranking.objects.create(container=competition,username='manu',points=10)
    # Ranking.objects.create(container=competition,username='pepe',points=1)
    # Ranking.objects.create(container=competition,username='lolo',points=5)
    
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

    response = HttpResponse(render_to_string('python.py', {'title': competition.title}))
    response['Content-Disposition'] = 'attachment; filename="%s.py"' % competition.title

    # Creating ranking if someone participates
    # User data updated below
    user = Profile.objects.filter(user=request.user)
    
    # Initializing user as participant
    ranking = Ranking.objects.filter(container=competition)
    username = request.user.username

    if ranking is None: ranking.create(container=competition)
    
    if ranking.filter(container=competition, username=username).exists() == False: 
        ranking.create(container=competition, username=username)
        user.update(points=F('points')+5)

    if user.filter(points__gte=25): user.update(challenger=True)

    competition.participants = ranking.count()
    competition.save()

    return response
