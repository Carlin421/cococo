from django.shortcuts import render 
from django.http import HttpResponseRedirect
from .models import CompanyPost, ActivityPost,User
from . import forms
# Create your views here.
from django.contrib.sessions.models import Session
from django.contrib import messages

def register(request):
	post_form = forms.RegisterForm()
	if 'user_name' in request.session:
		username = request.session['user_name']
	else:
		username = None
	if request.method == "POST":
		post_form = forms.RegisterForm(request.POST)
		if post_form.is_valid():
			post_form.save()
			request.session['user_name'] = post_form.cleaned_data['name']
			message = "儲存成功"
			return HttpResponseRedirect("/")
		else:
			message = "欄位皆必填"
	else:
		post_form = forms.RegisterForm()
		message = "欄位皆必填"
  
	return render(request , "register.html" , locals())
def login(request):
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST["user_name"].strip()
            password = request.POST["password"]
            try:
                user = User.objects.get(name = username)
                if user.password == password:
                    request.session['user_name'] = user.name
                    request.session['useremail'] = user.email
                    messages.add_message(request, messages.SUCCESS, '登入成功')
                    return HttpResponseRedirect("/")
                else:
                    messages.add_message(request, messages.WARNING, "密碼輸入錯誤")
            except:
                messages.add_message(request, messages.WARNING, "查無此帳號")
        else:
            messages.add_message(request, messages.INFO, "請檢查填寫資料")
    else:
        login_form = forms.LoginForm()
    
    return render(request , "login.html" , locals())

def userinfo(request):
    if 'user_name' in request.session:
        username = request.session['user_name']
        useremail = request.session['useremail']
    else:
        return HttpResponseRedirect("/")
    return render(request , "userinfo.html" , locals())


def logout(request):
    if 'user_name' in request.session:
        Session.objects.all().delete()
    return HttpResponseRedirect("/")
def homepage(request):
    posts = ActivityPost.objects.all()
    cposts = CompanyPost.objects.all()
    if 'user_name' in request.session:
        username = request.session['user_name']
    else:
        username = None
    return render(request,'index.html',locals())


def activity(request):
    posts = ActivityPost.objects.all()
    if 'user_name' in request.session:
        username = request.session['user_name']
    else:
        username = None

    return render(request,'ac_index.html',locals())

def create_activity(request):
	post_form = forms.PostForm()
	if 'user_name' in request.session:
		username = request.session['user_name']
	else:
		username = None
	if request.method == "POST":
		post_form = forms.PostForm(request.POST)
		if post_form.is_valid():
			post_form.save()
			message = "儲存成功"
			return HttpResponseRedirect("/")
		else:
			message = "欄位皆必填"
	else:
		post_form = forms.PostForm()
		message = "欄位皆必填"

	return render(request , "create_activity.html" , locals())

def company(request):
    posts = CompanyPost.objects.all()
    if 'user_name' in request.session:
        username = request.session['user_name']
    else:
        username = None
    return render(request,'cp_index.html',locals())

def create_company(request):
	post_form = forms.CompanyForm()
	if 'user_name' in request.session:
		username = request.session['user_name']
	else:
		username = None
	if request.method == "POST":
		post_form = forms.CompanyForm(request.POST)
		if post_form.is_valid():
			post_form.save()
			message = "儲存成功"
			return HttpResponseRedirect("/")
		else:
			message = "欄位皆必填"
	else:
		post_form = forms.CompanyForm()
		message = "欄位皆必填"
	return render(request , "create_company.html" , locals())