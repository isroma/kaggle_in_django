from django.forms import ModelForm
from django import forms
from dashboard.models import Dashboard
from django.utils import timezone
from bootstrap_datepicker_plus import DatePickerInput

class CompetitionForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Título")
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), label="Descripción")
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

    class Meta:
        model = Dashboard
        fields = ['title', 'description', 'beginning', 'deadline']
        exclude = ['participants', 'author']
