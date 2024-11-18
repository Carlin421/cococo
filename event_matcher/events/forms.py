from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Activitynew,Sponsorshipnew,UserProfile

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        
        if password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
          
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activitynew
        fields = ['title', 'description', 'location', 'date', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
class SponsorshipForm(forms.ModelForm):
    class Meta:
        model = Sponsorshipnew
        fields = ['title', 'description', 'amount', 'location', 'image']