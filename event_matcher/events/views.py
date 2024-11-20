from django.shortcuts import render,get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, RegisterForm,UserPhotoForm
from .models import Activitynew,Sponsorshipnew,UserProfile
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from django.db.models import Q
from .forms import ActivityForm
from .forms import SponsorshipForm
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def chatbot_view(request):
    return render(request, 'events/chatbot.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        form_userprofile = UserPhotoForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid() and form_userprofile.is_valid():
            form.save()
            form_userprofile.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
        form_userprofile = UserPhotoForm(instance=request.user.profile)

    context = {
        'form': form,
        'form_userprofile': form_userprofile
    }
    return render(request, 'events/edit_profile.html', context)
def user_profile(request, user_id):
    User= get_user_model()
    user = get_object_or_404(User, id=user_id)
    user_extend = UserProfile.objects.get(user=user)
    user_activities = Activitynew.objects.filter(organizer=user)
    context = {
        'user': user,
        'user_extend': user_extend,
        'user_activities': user_activities
    }
    return render(request, 'events/user_profile.html', context)

@login_required
def toggle_sponsorship_check(request, event_id):
    event = get_object_or_404(Sponsorshipnew, id=event_id)
    event.check_status = not event.check_status
    event.save()
    return redirect('check_activity')

@login_required
def toggle_activity_check(request, event_id):
    event = get_object_or_404(Activitynew, id=event_id)
    event.check_status = not event.check_status
    event.save()
    return redirect('check_activity')

@login_required
def check_activity(request) :
    if request.user.is_staff:
        activities = Activitynew.objects.all()
        sponsorships = Sponsorshipnew.objects.all()
        context = {
            'activities': activities,
            'sponsorships': sponsorships
        }
        # 如果是 Staff，用特定的方式顯示
        sponsorships = Sponsorshipnew.objects.all().order_by('-date_posted')
        return render(request, 'events/check_activity.html', context)
    else:
        # 如果不是 Staff，顯示其他內容或重定向
        return redirect('event_list')

@login_required
def check_sponsorship(request) :
    if request.user.is_staff:
        activities = Activitynew.objects.all()
        sponsorships = Sponsorshipnew.objects.all()
        context = {
            'activities': activities,
            'sponsorships': sponsorships
        }
        # 如果是 Staff，用特定的方式顯示
        sponsorships = Sponsorshipnew.objects.all().order_by('-date_posted')
        return render(request, 'events/check_sponsorship.html', context)
    else:
        # 如果不是 Staff，顯示其他內容或重定向
        return redirect('event_list')


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
        form_userprofile = UserPhotoForm(request.POST, request.FILES)
        if form.is_valid() and form_userprofile.is_valid():
            user = form.save()
            user_profile = form_userprofile.save(commit=False)
            user_profile.user = user
            user_profile.save()
            return redirect('login')  # 註冊完成後重定向到登入頁面
    else:
        form = RegisterForm()
        form_userprofile = UserPhotoForm()

    return render(request, 'events/register.html',{'form': form,'form_userprofile': form_userprofile})

def activitynew_list(request):
    query = request.GET.get('q')
    activities = Activitynew.objects.all()

    if query:
        activities = activities.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(date__icontains=query)
        )

    context = {
        'activity_list': activities,
        'query': query
    }
    return render(request, 'events/activitynew_list.html', context)
# @login_required
# def toggle_activitynew_favorite(request, activity_id):
#     activity = get_object_or_404(Activitynew, id=activity_id)
#     activity.is_favorited = not activity.is_favorited
#     activity.save()
#     return redirect('activitynew_list')

def sponsorship_list(request, page=1):
    sponsorships = Sponsorshipnew.objects.all().order_by('-date_posted')
    paginator = Paginator(sponsorships, 10)  # 每頁顯示 10 個項目
    
    try:
        sponsorships = paginator.page(page)
    except PageNotAnInteger:
        sponsorships = paginator.page(1)
    except EmptyPage:
        sponsorships = paginator.page(paginator.num_pages)
    
    return render(request, 'events/sponsorship_list.html', {'sponsorships': sponsorships})

# @login_required
# def toggle_sponsorshipnew_favorite(request, sponsorship_id):
#     sponsorship = get_object_or_404(Sponsorshipnew, id=sponsorship_id)
#     sponsorship.is_favorited = not sponsorship.is_favorited
#     sponsorship.save()
#     return redirect('sponsorship_list')

def custom_logout(request):
    logout(request)
    # 如果您使用了任何自定義的認證令牌，在這裡清除它們
    # 例如：request.user.auth_token.delete()
    return redirect('event_list')  # 或者您希望重定向到的任何頁面


@login_required
def profile_view(request):
    # 獲取用戶收藏的活動和贊助
    favorite_activities = Activitynew.objects.filter(is_favorited=True)
    favorite_sponsorships = Sponsorshipnew.objects.filter(is_favorited=True)
    
    # 獲取用戶發布的活動
    user_activities = Activitynew.objects.filter(organizer=request.user)
    
    # 用戶的照片跟描述
    user_extend = UserProfile.objects.get(user=request.user)
    context = {
        'favorite_activities': favorite_activities,
        'favorite_sponsorships': favorite_sponsorships,
        'user_activities': user_activities,
        'user_extend': user_extend
    }
    return render(request, 'events/profile.html', context)
def sponsor_detail(request, sponsorship_id):
    sponsorship = get_object_or_404(Sponsorshipnew, pk=sponsorship_id)
    return render(request, 'events/sponsor_detail.html', {'sponsorship': sponsorship})
def activity_detail(request, activity_id):
    activity = get_object_or_404(Activitynew, pk=activity_id)
    return render(request, 'events/activity_detail.html', {'activity': activity})
def about_us(request):
    return render(request, 'events/aboutus.html')

@login_required
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.organizer = request.user  # 假設您的 Activitynew 模型有一個 organizer 字段
            activity.save()
            messages.success(request, '活動已成功創建!')
            return redirect('activity_detail', activity_id=activity.id)
    else:
        form = ActivityForm()
    return render(request, 'events/add_activity.html', {'form': form})

@login_required
def add_sponsorship(request):
    if request.method == 'POST':
        form = SponsorshipForm(request.POST, request.FILES)
        if form.is_valid():
            sponsorship = form.save(commit=False)
            sponsorship.sponsor = request.user
            sponsorship.save()
            messages.success(request, '贊助已成功創建!')
            return redirect('sponsor_detail', sponsorship_id=sponsorship.id)
    else:
        form = SponsorshipForm()
    return render(request, 'events/add_sponsorship.html', {'form': form})