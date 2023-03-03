from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from actors.model.actor import Chauffeur, Client

#Formulaire du Login (Front End)
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Utilisateur", 
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder':"Nom d'utilisateur"}))

    password = forms.CharField(
        label="Mot de passe",
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder':'Mot de passe'}))

class NewUserForm(UserCreationForm):
    last_name = forms.CharField(
        label="Prénom", 
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name', 'placeholder':"Prénom"}))
    first_name = forms.CharField(
        label="Nom", 
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name', 'placeholder':"Nom"}))
    email = forms.EmailField(
        required=True,
        label="Adresse email",
        max_length=30,
        widget=forms.EmailInput(attrs={'class':'form-control', 'name':'email', 'placeholder':'Adresse email'})
        )
    password1 = forms.CharField(
        label="Mot de passe",
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password1', 'placeholder':'Mot de passe'}))
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password2', 'placeholder':'Confirmation du mot de passe'}))
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    phone = forms.CharField(
        label="téléphone",
        # validators = [phoneNumberRegex], 
        max_length = 16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'phone', 'placeholder':"Téléphone"})
        )    
    class Meta:
        model = Chauffeur
        fields = ("first_name", "last_name", "email", "password1", "password2","phone")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.username = user.email
        if commit:
            user.save()
        return user


class NewClientForm(UserCreationForm):
    last_name = forms.CharField(
        label="Prénom", 
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name', 'placeholder':"Prénom"}))
    first_name = forms.CharField(
        label="Nom", 
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name', 'placeholder':"Nom"}))
    email = forms.EmailField(
        required=True,
        label="Adresse email",
        max_length=30,
        widget=forms.EmailInput(attrs={'class':'form-control', 'name':'email', 'placeholder':'Adresse email'})
        )
    password1 = forms.CharField(
        label="Mot de passe",
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password1', 'placeholder':'Mot de passe'}))
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password2', 'placeholder':'Confirmation du mot de passe'}))
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    phone = forms.CharField(
        label="téléphone",
        # validators = [phoneNumberRegex], 
        max_length = 16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'phone', 'placeholder':"Téléphone"})
        )    
    class Meta:
        model = Client
        fields = ("first_name", "last_name", "email", "password1", "password2","phone")

    def save(self, commit=True):
        user = super(NewClientForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.username = user.email
        if commit:
            user.save()
        return user

