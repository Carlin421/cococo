from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Activitynew,Sponsorshipnew,UserProfile
from django.contrib.auth.hashers import make_password


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
    role = forms.ChoiceField(choices=[('brand', '品牌方'), ('club', '社團方')], required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        labels = {
            'username': '使用者名稱',
            'email': '電子郵件',
            'password': '密碼',
            'role': '角色',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self.add_error('password_confirm', "密碼不匹配。")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # 创建 UserProfile 并设置角色
            UserProfile.objects.create(user=user, role=self.cleaned_data['role'])
        return user

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
        fields = ['title', 'description','max_participants','current_participants', 'location', 'date','registration_deadline', 'image','latitude', 'longitude']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'registration_deadline':forms.DateInput(attrs={'type': 'date'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
        labels = {
            'title': '活動標題',          
            'description': '活動描述',  
            'max_participants':'參與人數上限',
            'current_participants':'目前報名人數',
            'location': '活動位置',    
            'date': '活動日期',
            'registration_deadline': '截止日期',              
            'image': '活動圖片',           
        }
class SponsorshipForm(forms.ModelForm):
    class Meta:
        model = Sponsorshipnew
        fields = ['title', 'description', 'item','amount','people', 'location', 'image']
        labels = {
            'title': '贊助標題',          
            'description': '贊助介紹',
            'item':'贊助商品',
            'people': '宣傳模式',
            'amount': '贊助金額',        
            'location': '贊助地點',      
            'image': '贊助圖片',     
        }