from django.forms import ModelForm
from django import forms
from dashboard.models import Dashboard, Ranking
from django.utils import timezone
from bootstrap_datepicker_plus import DatePickerInput


class CompetitionForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    beginning = forms.DateField(widget=DatePickerInput(format='%d/%m/%Y', options={
        "showClose": False,
        "showClear": False,
        "showTodayButton": False,
    }), initial=timezone.now())
    deadline = forms.DateField(widget=DatePickerInput(format='%d/%m/%Y', options={
        "showClose": False,
        "showClear": False,
        "showTodayButton": False,
    }), initial=timezone.now())
    train = forms.FileField(widget=forms.FileInput())
    test = forms.FileField(widget=forms.FileInput())
    max_daily_uploads = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'number'}), initial=5)
    wait_time_uploads = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'number'}), initial=60)

    class Meta:
        model = Dashboard
        fields = ['title', 'description', 'beginning', 'deadline', 'train', 'test', 'max_daily_uploads', 'wait_time_uploads']
        exclude = ['predictions', 'participants', 'author']


class SubmissionForm(ModelForm):
    submission = forms.FileField(widget=forms.FileInput())

    class Meta:
        model = Ranking
        fields = ['submission']
        exclude = ['container', 'username', 'points']