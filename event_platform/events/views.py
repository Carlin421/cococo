from django.shortcuts import render, redirect
from .models import Event,Profile
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db import IntegrityError




def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

# 找活動頁面
def find_events(request):
    return render(request, 'events/find_events.html')

def find_sponsorships(request):
    return render(request, 'events/find_sponsorships.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('event_list')  # 登入後重定向至活動列表
        else:
            messages.error(request, '帳號或密碼錯誤')
    
    return render(request, 'events/login.html')

def user_logout(request):
    logout(request)
    return redirect('event_list')  # 登出後重定向至活動列表


# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user_type = request.POST['user_type']

#         if User.objects.filter(username=username).exists():
#             messages.error(request, '帳號已存在')
#         else:
#             user = User.objects.create_user(username=username, password=password)
#             user.profile.user_type = user_type  # 假設我們擁有 user_type 欄位
#             user.save()
#             messages.success(request, '註冊成功，請登入')
#             return redirect('login')

#     return render(request, 'events/register.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')

        # 驗證帳號及電子郵件的唯一性
        if User.objects.filter(username=username).exists():
            messages.error(request, '帳號已存在')
        elif Profile.objects.filter(email=email).exists():
            messages.error(request, '該電子郵件已被使用')
        else:
            try:
                # 建立新用戶
                user = User.objects.create_user(username=username, password=password)
                user.email = email  # 設置 email
                user.save()

                # 建立 Profile
                Profile.objects.create(user=user, email=email, user_type=user_type)

                messages.success(request, '註冊成功，請登入')
                return redirect('login')
            except IntegrityError:
                messages.error(request, '該電子郵件已存在於系統中')

    return render(request, 'events/register.html')


