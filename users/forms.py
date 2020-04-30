from django import forms
from django.forms import ModelForm
from users.models import Profile
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Nombre de usuario")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Contraseña")
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Repetir contraseña")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_repeat']

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Nombre de usuario")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Contraseña")

    class Meta:
        model = User
        fields = ['username', 'password']
        exclude = ['email', 'password_repeat']

class ProfileForm(ModelForm):
    verified = forms.BooleanField(widget=forms.HiddenInput(), initial=False)

    class Meta:
        model = Profile
        fields = ['verified']
