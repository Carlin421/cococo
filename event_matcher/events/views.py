from django.shortcuts import render,get_object_or_404, redirect
from events.models import Activity, Sponsorship
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, RegisterForm
from .models import Activitynew,Sponsorshipnew

def activity_list(request):
    activities = Activity.objects.all()
    sponsorships = Sponsorship.objects.all()
    context = {
        'activities': activities,
        'sponsorships': sponsorships
    }
    return render(request, 'events/event_list.html', context)


def toggle_activity_favorite(request, event_id):
    event = get_object_or_404(Activity, id=event_id)
    event.is_favorited = not event.is_favorited
    event.save()
    return redirect('activity_list')

# 用於贊助的收藏切換
def toggle_sponsorship_favorite(request, sponsorship_id):
    
    sponsorship = get_object_or_404(Sponsorship, id=sponsorship_id)
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

def toggle_activitynew_favorite(request, activity_id):
    activity = get_object_or_404(Activitynew, id=activity_id)
    activity.is_favorited = not activity.is_favorited
    activity.save()
    return redirect('activitynew_list')


def sponsorship_list(request):
    sponsorship_list = Sponsorshipnew.objects.all()
    return render(request, 'events/sponsorship_list.html', {'sponsorship_list': sponsorship_list})


def toggle_sponsorshipnew_favorite(request, sponsorship_id):
    sponsorship = get_object_or_404(Sponsorshipnew, id=sponsorship_id)
    sponsorship.is_favorited = not sponsorship.is_favorited
    sponsorship.save()
    return redirect('sponsorship_list')

# Create your views here.
