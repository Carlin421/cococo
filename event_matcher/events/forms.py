from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Activitynew,Sponsorshipnew,UserProfile

class UserPhotoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo', 'description']
        labels = {
            'photo': '照片',
            'description': '描述',  # 如果也想改 description 的标签
        }
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': '照片',
            'email': '電子郵件',
            'password': '密碼',
        }

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
        labels = {
            'username': '照片',
            'email': '電子郵件',
        }
          
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activitynew
        fields = ['title', 'description', 'location', 'date', 'image','latitude', 'longitude']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
        labels = {
            'title': '活動標題',          
            'description': '活動描述',    
            'location': '活動位置',    
            'date': '活動日期',          
            'image': '活動圖片',           
        }
class SponsorshipForm(forms.ModelForm):
    class Meta:
        model = Sponsorshipnew
        fields = ['title', 'description', 'amount', 'location', 'image']
        labels = {
            'title': '贊助標題',          
            'description': '贊助描述',   
            'amount': '贊助金額',        
            'location': '贊助地點',      
            'image': '贊助圖片',     
        }