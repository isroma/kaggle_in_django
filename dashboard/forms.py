from django.forms import ModelForm
from django import forms
from dashboard.models import Dashboard
from django.utils import timezone
from bootstrap_datepicker_plus import DatePickerInput


class CompetitionForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), label="Título")
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}), label="Descripción")
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
    max_daily_uploads = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'number'}),
        label="Envíos diarios permitidos", initial=5)
    wait_time_uploads = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'number'}),
        label="Tiempo de espera entre envíos", initial=60)

    class Meta:
        model = Dashboard
        fields = ['title', 'description', 'beginning', 'deadline', 'max_daily_uploads', 'wait_time_uploads']
        exclude = ['participants', 'author']
