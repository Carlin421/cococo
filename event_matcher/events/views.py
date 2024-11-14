from django.shortcuts import render,get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, RegisterForm
from .models import Activitynew,Sponsorshipnew
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm

def activity_list(request):
    activities = Activitynew.objects.all()
    sponsorships = Sponsorshipnew.objects.all()
    context = {
        'activities': activities,
        'sponsorships': sponsorships
    }
    return render(request, 'events/event_list.html', context)

@login_required
def toggle_activity_favorite(request, event_id):
    event = get_object_or_404(Activitynew, id=event_id)
    event.is_favorited = not event.is_favorited
    event.save()
    return redirect('activity_list')

# 用於贊助的收藏切換
@login_required
def toggle_sponsorship_favorite(request, sponsorship_id):
    
    sponsorship = get_object_or_404(Sponsorshipnew, id=sponsorship_id)
    sponsorship.is_favorited = not sponsorship.is_favorited
    sponsorship.save()
    return redirect('activity_list')
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('event_list')  # 登入成功後的導向頁面
    else:
        form = LoginForm()
    return render(request, 'events/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            role = request.POST.get("role")
            # 根據 role 進行不同的處理，例如存儲到用戶的其他屬性
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'events/register.html', {'form': form})


def activitynew_list(request):
    activitynew_list = Activitynew.objects.all()  # 使用新的變數名稱
    return render(request, 'events/activitynew_list.html', {'activitynew_list': activitynew_list})
@login_required
def toggle_activitynew_favorite(request, activity_id):
    activity = get_object_or_404(Activitynew, id=activity_id)
    activity.is_favorited = not activity.is_favorited
    activity.save()
    return redirect('activitynew_list')


def sponsorship_list(request):
    sponsorship_list = Sponsorshipnew.objects.all()
    return render(request, 'events/sponsorship_list.html', {'sponsorship_list': sponsorship_list})

@login_required
def toggle_sponsorshipnew_favorite(request, sponsorship_id):
    sponsorship = get_object_or_404(Sponsorshipnew, id=sponsorship_id)
    sponsorship.is_favorited = not sponsorship.is_favorited
    sponsorship.save()
    return redirect('sponsorship_list')

def custom_logout(request):
    logout(request)
    # 如果您使用了任何自定義的認證令牌，在這裡清除它們
    # 例如：request.user.auth_token.delete()
    return redirect('event_list')  # 或者您希望重定向到的任何頁面


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'events/profile.html', {'form': form})

def sponsor_detail(request, sponsor_id):
    sponsor = get_object_or_404(Sponsorshipnew, pk=sponsor_id)
    return render(request, 'events/sponsor_detail.html', {'sponsor': sponsor})

def activity_detail(request, activity_id):
    activity = get_object_or_404(Activitynew, pk=activity_id)
    return render(request, 'events/activity_detail.html', {'activity': activity})