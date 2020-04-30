from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Nombre de usuario")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Contraseña")
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Repetir contraseña")

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Nombre de usuario")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Contraseña")
