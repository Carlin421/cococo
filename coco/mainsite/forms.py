from django import forms
from . import models
from captcha.fields import CaptchaField

class PostForm(forms.ModelForm):
	# captcha = CaptchaField()
	class Meta:
		model = models.ActivityPost
		fields = ['title','content']
	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['title'].label = '活動標題'
		self.fields['content'].label = '活動內容'
		# self.fields['captcha'].label = '不是機器人'
  
class CompanyForm(forms.ModelForm):
	# captcha = CaptchaField()
	class Meta:
		model = models.CompanyPost
		fields = ['title','content']
	def __init__(self, *args, **kwargs):
		super(CompanyForm, self).__init__(*args, **kwargs)
		self.fields['title'].label = '公司名稱'
		self.fields['content'].label = '贊助內容'
		# self.fields['captcha'].label = '不是機器人'

class RegisterForm(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = models.User
		fields = ['name','email','password']
	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = '名字'
		self.fields['email'].label = 'email'
		self.fields['password'].label = '密碼'
		self.fields['captcha'].label = '不是機器人'
class LoginForm(forms.Form):
	user_name = forms.CharField(label = '姓名', max_length=50)
	password =forms.CharField(label = '密碼', widget=forms.PasswordInput)