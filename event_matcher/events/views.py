from django.shortcuts import render,get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, RegisterForm,UserPhotoForm
from .models import Activitynew,Sponsorshipnew,UserProfile, Favorite ,SponsorshipInterest
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from django.db.models import Q
from .forms import ActivityForm
from .forms import SponsorshipForm
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from firebase_admin import firestore
from .models import Notification
from django.db.models import Exists, OuterRef
from django.db import IntegrityError
import logging
from django.views.decorators.http import require_POST
logger = logging.getLogger(__name__)

@login_required
def choose_activity(request, sponsorship_id):
    sponsorship = get_object_or_404(Sponsorshipnew, id=sponsorship_id)
    events = Activitynew.objects.filter(organizer=request.user)  # 假設活動是用 owner/user 綁定的

    if request.method == 'POST' :
        event_id = request.POST.get('event_id')
        print(event_id)
        if not event_id:
            messages.error(request, '請選擇活動')
            return redirect('choose_activity', sponsorship_id=sponsorship_id)
        else:
            event = get_object_or_404(Activitynew, id=event_id)

            SponsorshipInterest.objects.get_or_create(
                user=request.user,
                event=event,
                sponsorship=sponsorship
            )

            # # 傳送訊息
            # message = f"我對贊助《{sponsorship.title}》有興趣，想用活動《{event.title}》參加！"
            # return redirect(f"/chatroom/?msg={message}")
            return (redirect('sponsor_detail', sponsorship_id=sponsorship_id))

    return render(request, 'events/choose_activity.html', {
        'sponsorship': sponsorship,
        'events': events
    })


@login_required
def check_profile_completion(request):
    user_profile = request.user.profile
    if request.user.social_auth.filter(provider='google-oauth2').exists():
        if not user_profile.role or not user_profile.description:
            messages.warning(request, '請完成您的個人資料設置。')
            return redirect('edit_profile')
    return redirect('event_list')  # 或其他適當的主頁
# 在 event_matcher/events/views.py 文件中
def notifications(request):    
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
        unread_count = notifications.filter(is_read=False).count()
        return {
            'notifications': notifications,
            'unread_notifications_count': unread_count
        }
    return {}
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'events/notification_list.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')
@login_required
def chatroom_list(request):
    db = firestore.client()
    chatrooms = db.collection('chatrooms').where('members', 'array_contains', request.user.username).get()
    
    chatroom_data = []
    for chat in chatrooms:
        chat_dict = chat.to_dict()
        other_user = next((user for user in chat_dict['members'] if user != request.user.username), None)
        
        # 檢查是否有消息，如果沒有，設置一個默認值
        messages = chat_dict.get('messages', {})
    
    # 導回通知列表
        if messages:
            last_message_key = max(messages, key=lambda k: messages[k]['timestamp'])
            last_message = messages[last_message_key].get('content', '暫無消息')
        else:
            last_message = '暫無消息'
        
        chatroom_data.append({
            'id': chat.id,
            'other_user': other_user,
            'last_message': last_message
        })
    
    return render(request, 'events/chatroom_list.html', {'chatrooms': chatroom_data})
@login_required
def chatroom(request, chat_id):
    db = firestore.client()
    chat_ref = db.collection('chatrooms').document(chat_id)
    chat_data = chat_ref.get().to_dict()
    
    if request.user.username not in chat_data['members']:
        return redirect('home')  # 或其他適當的錯誤處理
    
    other_user = next(user for user in chat_data['members'] if user != request.user.username)
    
    # 獲取當前用戶的名稱
    current_user_name = request.user.get_full_name() or request.user.username
    
    context = {
        'chat_id': chat_id,
        'other_user': other_user,
        'messages': chat_data.get('messages', {}),
        'chat_name': f"與 {other_user} 的聊天",
        'current_user_name': current_user_name  # 添加當前用戶名稱到上下文
    }
    return render(request, 'events/chatroom.html', context)
def chatbot_view(request):
    return render(request, 'events/chatbot.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        form_userprofile = UserPhotoForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid() and form_userprofile.is_valid():
            form.save()
            profile = form_userprofile.save(commit=False)
            
            # 檢查身分別是否有變更
            old_role = request.user.profile.role
            new_role = form_userprofile.cleaned_data['role']
            
            if old_role != new_role:
                messages.info(request, f'您的身分別已從 {old_role} 更改為 {new_role}')
            
            profile.save()
            messages.success(request, '個人檔案已經更新')
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
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    user_extend = UserProfile.objects.get(user=user)
    user_activities = Activitynew.objects.filter(organizer=user)
    user_sponsorships = Sponsorshipnew.objects.filter(organizer=user)
    # 檢查聊天室是否存在
    db = firestore.client()
    chat_id = get_or_create_chat(request.user.username, user.username)

    context = {
        'user': user,
        'user_extend': user_extend,
        'user_activities': user_activities,
        'user_sponsorships':user_sponsorships,
        'chat_id': chat_id
    }
    return render(request, 'events/user_profile.html', context)

def get_or_create_chat(user1, user2):
    db = firestore.client()
    chats_ref = db.collection('chatrooms')
    
    # 檢查是否已存在聊天室
    query = chats_ref.where('members', 'array_contains', user1).get()
    for chat in query:
        if user2 in chat.to_dict()['members']:
            return chat.id

    # 如果不存在，創建新的聊天室
    new_chat_ref = chats_ref.document()
    new_chat_ref.set({
        'members': [user1, user2],
        'createtime': firestore.SERVER_TIMESTAMP
    })
    return new_chat_ref.id
@login_required
def toggle_sponsorship_check(request, event_id):
    event = get_object_or_404(Sponsorshipnew, id=event_id)
    if request.user.is_staff:
        event.check_status = not event.check_status
        event.save()
        status = "通過審核" if event.check_status else "取消審核"
        messages.success(request, f'贊助 "{event.title}" 已{status}')
    else:
        messages.error(request, '您沒有權限執行此操作')
    
    # 使用 HTTP_REFERER 返回到之前的頁面
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        # 如果沒有 referer，則重定向到一個默認頁面
        return redirect('sponsorship_list')  # 或者其他適當的頁面

@login_required
def toggle_activity_check(request, event_id):
    event = get_object_or_404(Activitynew, id=event_id)
    event.check_status = not event.check_status
    event.save()
    return redirect('check_activity')

@login_required
def check_activity(request) :
    if request.user.is_staff:
        activities = list(Activitynew.objects.all().order_by('-date_posted'))  # 強制排序
        sponsorships = list(Sponsorshipnew.objects.all().order_by('-date_posted') ) # 強制排序
        context = {
            'activities': activities,
            'sponsorships': sponsorships
        }
        # 如果是 Staff，用特定的方式顯示
        return render(request, 'events/check_activity.html', context)
    else:
        # 如果不是 Staff，顯示其他內容或重定向
        return redirect('event_list')

@login_required
def check_sponsorship(request) :
    if request.user.is_staff:
        activities = list(Activitynew.objects.all().order_by('-date_posted'))
        sponsorships = list(Sponsorshipnew.objects.all().order_by('-date_posted') )
        context = {
            'activities': activities,
            'sponsorships': sponsorships
        }
        # 如果是 Staff，用特定的方式顯示
        return render(request, 'events/check_sponsorship.html', context)
    else:
        # 如果不是 Staff，顯示其他內容或重定向
        return redirect('event_list')


def activity_list(request):


    activities = Activitynew.objects.filter(check_status=True, is_active=True)
    sponsorships = Sponsorshipnew.objects.filter(check_status=True, is_active=True)



    # 添加收藏狀態
    if request.user.is_authenticated:
        activities = activities.annotate(
            is_favorited=Exists(
                Favorite.objects.filter(
                    user=request.user,
                    activity=OuterRef('pk')
                )
            )
        )
        sponsorships = sponsorships.annotate(
            is_favorited=Exists(
                Favorite.objects.filter(
                    user=request.user,
                    sponsorship=OuterRef('pk')
                )
            )
        )


    return render(request, 'events/event_list.html', {'activities': activities, 'sponsorships': sponsorships})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Activitynew, Sponsorshipnew, Favorite

@login_required
@require_POST
def toggle_activity_favorite(request, event_id):
    try:
        activity = get_object_or_404(Activitynew, id=event_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, activity=activity)
        
        if not created:
            favorite.delete()
            is_favorited = False
        else:
            is_favorited = True
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'is_favorited': is_favorited})
        else:
            return redirect(request.META.get('HTTP_REFERER', 'activitynew_list'))
    except IntegrityError:
        logger.error(f"IntegrityError for user {request.user.id} and activity {event_id}")
        return JsonResponse({'status': 'error', 'message': 'Database integrity error'}, status=500)
    except Exception as e:
        logger.error(f"Error in toggle_activity_favorite: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred'}, status=500)

@login_required
@require_POST
def toggle_sponsorship_favorite(request, sponsorship_id):
    try:
        sponsorship = get_object_or_404(Sponsorshipnew, id=sponsorship_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, sponsorship=sponsorship)
        
        if not created:
            favorite.delete()
        
        is_favorited = created  # 如果創建了新的收藏，則為 True；否則為 False

        return JsonResponse({
            'status': 'success',
            'is_favorited': is_favorited
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
def is_favorited(user, obj):
    if not user.is_authenticated:
        return False
    if isinstance(obj, Activitynew):
        return Favorite.objects.filter(user=user, activity=obj).exists()
    elif isinstance(obj, Sponsorshipnew):
        return Favorite.objects.filter(user=user, sponsorship=obj).exists()
    return False
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

from django.db import IntegrityError
from django.shortcuts import render, redirect
from events.models import UserProfile

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form_userprofile = UserPhotoForm(request.POST, request.FILES)
        if form.is_valid() and form_userprofile.is_valid():
            try:
                # 創建 User
                user = form.save()

                # 嘗試創建 UserProfile
                user_profile = form_userprofile.save(commit=False)
                user_profile.user = user
                user_profile.role = form.cleaned_data['role']  # 保存用戶角色
                user_profile.save()

                return redirect('login')  # 註冊完成後重定向到登入頁面

            except IntegrityError:
                # 如果出現唯一性錯誤，說明用戶已存在
                form.add_error(None, "A profile for this user already exists.")

    else:
        form = RegisterForm()
        form_userprofile = UserPhotoForm()

    return render(request, 'events/register.html', {'form': form, 'form_userprofile': form_userprofile})


def activitynew_list(request):
    query = request.GET.get('q')
    if request.user.is_staff:
        activities = Activitynew.objects.all()
    else:
        activities = Activitynew.objects.filter(check_status=True, is_active=True)
    

    if query:
        activities = activities.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(date__icontains=query)
        )
    
    if request.user.is_authenticated:
        for activity in activities:
            activity.is_favorited = activity.favorite_set.filter(user=request.user).exists()
    else:
        for activity in activities:
            activity.is_favorited = False
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

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.db.models import Q

def sponsorship_list(request, page=1):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', '')
    amount = request.GET.get('amount', None)
    organizer = request.GET.get('organizer', None)

    if request.user.is_staff:
        sponsorships = Sponsorshipnew.objects.all()
    else:
        sponsorships = Sponsorshipnew.objects.filter(check_status=True, is_active=True)

    # 搜索功能
    if query:
        sponsorships = sponsorships.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(date_posted__icontains=query)
        )

    # 金額篩選
    if amount:
        sponsorships = sponsorships.filter(amount__lte=amount)

    # 品牌篩選
    if organizer:
        sponsorships = sponsorships.filter(organizer__iexact=organizer)

    # 排序功能
    if sort == 'date_posted_asc':
        sponsorships = sponsorships.order_by('date_posted')
    elif sort == 'date_posted_desc':
        sponsorships = sponsorships.order_by('-date_posted')

    # 獲取所有品牌名稱
    brands = Sponsorshipnew.objects.values_list('organizer', flat=True).distinct()

    # 分頁處理
    paginator = Paginator(sponsorships, 10)
    try:
        sponsorships_page = paginator.page(page)
    except PageNotAnInteger:
        sponsorships_page = paginator.page(1)
    except EmptyPage:
        sponsorships_page = paginator.page(paginator.num_pages)

    context = {
        'sponsorships': sponsorships_page,
        'query': query,
        'sort': sort,
        'selected_amount': amount,
        'brands': brands,  # 傳遞品牌列表到模板
    }
    return render(request, 'events/sponsorship_list.html', context)




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
    user_extend, created = UserProfile.objects.get_or_create(user=request.user)
    # 獲取用戶收藏的活動和贊助
    favorite_activities = Activitynew.objects.filter(favorite__user=request.user)
    favorite_sponsorships = Sponsorshipnew.objects.filter(favorite__user=request.user)
    
    # 獲取用戶發布的活動和贊助
    user_activities = Activitynew.objects.filter(organizer=request.user)
    user_sponsorships = Sponsorshipnew.objects.filter(organizer=request.user)
    
    # 用戶的照片跟描述
    user_extend = UserProfile.objects.get(user=request.user)
    context = {
        'favorite_activities': favorite_activities,
        'favorite_sponsorships': favorite_sponsorships,
        'user_activities': user_activities,
        'user_sponsorships':user_sponsorships,
        'user_extend': user_extend
    }
    return render(request, 'events/profile.html', context)
def activity_detail(request, activity_id):
    activity = get_object_or_404(Activitynew, id=activity_id)
    is_fav = is_favorited(request.user, activity) if request.user.is_authenticated else False
    context = {'activity': activity, 'is_favorited': is_fav}
    return render(request, 'events/activity_detail.html', context)

def sponsor_detail(request, sponsorship_id):
    sponsorship = get_object_or_404(Sponsorshipnew, id=sponsorship_id)
    is_fav = is_favorited(request.user, sponsorship) if request.user.is_authenticated else False
    sponsorinterest_bool = SponsorshipInterest.objects.filter(user=request.user, sponsorship_id=sponsorship_id).exists()
    context = {'sponsorship': sponsorship, 'is_favorited': is_fav, 'sponsorinterest_bool': sponsorinterest_bool}
    sponsorinterest_bool = SponsorshipInterest.objects.filter(user=request.user, sponsorship_id=sponsorship_id).exists()
    return render(request, 'events/sponsor_detail.html', context)
def about_us(request):
    return render(request, 'events/aboutus.html')

@login_required
def add_activity(request):
    # Initialize `form` to ensure it is defined
    form = None

    # Check if the user is a club organizer
    if not request.user.profile.is_club:
        messages.error(request, '只有社團方可以新增活動。')
        return redirect('activitynew_list')  # Redirect to a suitable page, e.g., activity list

    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)  # Initialize form with POST data
        if not request.user.is_authenticated:
            messages.error(request, '請先登入才能創建活動。')
            return redirect('login')  # Redirect to login page

        if form.is_valid():  # Validate the form input
            activity = form.save(commit=False)
            activity.organizer = request.user
            activity.save()
            messages.success(request, '活動已成功創建!')

            # Create a notification
            Notification.objects.create(
                user=activity.organizer,
                activity=activity,
                message=f'您的活動"{activity.title}"已成功創建'
            )
            return redirect('activity_detail', activity_id=activity.id)
        else:
            messages.error(request, '請檢查表單是否正確填寫。')
    else:
        form = ActivityForm()  # Initialize a blank form for GET request

    # Render the form for both GET and POST requests
    return render(request, 'events/add_activity.html', {'form': form})


@login_required
def add_sponsorship(request):
    # Initialize the form to ensure it is defined in all cases
    form = None

    # Check if the user is a brand
    if not request.user.profile.is_brand:
        messages.error(request, '只有品牌方可以新增贊助。')
        return redirect('sponsorship_list')  # Redirect to an appropriate page

    if request.method == 'POST':
        form = SponsorshipForm(request.POST, request.FILES)  # Initialize form with POST data
        if not request.user.is_authenticated:
            messages.error(request, '請先登入才能創建贊助。')
            return redirect('login')  # Redirect to login page

        if not request.user.profile.is_brand:
            messages.error(request, '只有品牌方可以創建贊助。')
            return redirect('sponsorship_list')  # Redirect to sponsorship list
        elif form.is_valid():  # Validate form input
            sponsorship = form.save(commit=False)
            sponsorship.organizer = request.user
            sponsorship.save()
            messages.success(request, '贊助已成功創建!')

            # Create a notification
            Notification.objects.create(
                user=sponsorship.organizer,
                sponsorship=sponsorship,
                message=f'您的贊助"{sponsorship.title}"已成功創建'
            )
            return redirect('sponsor_detail', sponsorship_id=sponsorship.id)
        else:
            messages.error(request, '請檢查表單是否正確填寫。')
    else:
        form = SponsorshipForm()  # Default form for GET request

    return render(request, 'events/add_sponsorship.html', {'form': form})


@login_required
def toggle_activity_status(request, activity_id):
    activity = get_object_or_404(Activitynew, id=activity_id)
    if request.user == activity.organizer or request.user.is_staff:
        if activity.check_status:
            activity.is_active = not activity.is_active
            activity.save()
            status = "上架" if activity.is_active else "下架"
            messages.success(request, f'活動已{status}')
            
            # 創建通知
            Notification.objects.create(
                user=activity.organizer,
                activity=activity,
                message=f'您的活動 "{activity.title}" 已{status}'
            )
        else:
            messages.error(request, '活動尚未通過審核，無法更改狀態')
    else:
        messages.error(request, '您沒有權限執行此操作')
    return redirect('activity_detail', activity_id=activity.id)

@login_required
def edit_activity(request, activity_id):
    activity = get_object_or_404(Activitynew, id=activity_id)
    
    if request.user != activity.organizer:
        messages.error(request, '您沒有權限編輯此活動')
        return redirect('activity_detail', activity_id=activity.id)
    
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, '活動已成功更新')
            return redirect('activity_detail', activity_id=activity.id)
    else:
        form = ActivityForm(instance=activity)
    
    return render(request, 'events/edit_activity.html', {'form': form, 'activity': activity})
@login_required
def toggle_sponsorship_status(request, sponsorship_id):
    sponsorship = get_object_or_404(Sponsorshipnew, id=sponsorship_id)
    if request.user == sponsorship.organizer or request.user.is_staff:
        if sponsorship.check_status:
            sponsorship.is_active = not sponsorship.is_active
            sponsorship.save()
            status = "上架" if sponsorship.is_active else "下架"
            messages.success(request, f'贊助已{status}')
            
            # 創建通知
            Notification.objects.create(
                user=sponsorship.organizer,
                sponsorship=sponsorship,
                message=f'您的贊助 "{sponsorship.title}" 已{status}'
            )
        else:
            messages.error(request, '贊助尚未通過審核，無法更改狀態')
    else:
        messages.error(request, '您沒有權限執行此操作')
    return redirect('sponsor_detail', sponsorship_id=sponsorship.id)

@login_required
def edit_sponsorship(request, sponsorship_id):
    sponsorship = get_object_or_404(Sponsorshipnew, id=sponsorship_id)
    
    if request.user != sponsorship.organizer:
        messages.error(request, '您沒有權限編輯此贊助')
        return redirect('sponsor_detail', sponsorship_id=sponsorship.id)
    
    if request.method == 'POST':
        form = SponsorshipForm(request.POST, request.FILES, instance=sponsorship)
        if form.is_valid():
            form.save()
            messages.success(request, '贊助已成功更新')

            # 創建通知
            Notification.objects.create(
                user=sponsorship.organizer,
                sponsorship=sponsorship,
                message=f'贊助 "{sponsorship.title}" 已成功更新'
            )
            return redirect('sponsor_detail', sponsorship_id=sponsorship.id)
    else:
        form = SponsorshipForm(instance=sponsorship)
    
    return render(request, 'events/edit_sponsorship.html', {'form': form, 'sponsorship': sponsorship})

@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activitynew, id=activity_id)
    
    if request.user != activity.organizer and not request.user.is_staff:
        messages.error(request, '您沒有權限刪除此活動')
        return redirect('activity_detail', activity_id=activity.id)

    if request.method == 'POST':
        confirmation = request.POST.get('confirmation', '')
        if confirmation == activity.title:
            
            messages.success(request, '活動已成功刪除')
             # 創建通知
            Notification.objects.create(
                user=activity.organizer,
                message=f'活動 "{activity.title}" 已成功刪除'
            )
            activity.delete()
            
            return redirect('activitynew_list')  # 或其他適當的頁面
        else:
            messages.error(request, '確認文字不匹配，活動未被刪除')
    
    return render(request, 'events/delete_activity.html', {'activity': activity})

@login_required
def delete_sponsorship(request, sponsorship_id):
    sponsorship = get_object_or_404(Sponsorshipnew, id=sponsorship_id)
    
    if request.user != sponsorship.organizer and not request.user.is_staff:
        messages.error(request, '您沒有權限刪除此贊助')
        return redirect('sponsorship_detail', sponsorship_id=sponsorship_id)

    if request.method == 'POST':
        confirmation = request.POST.get('confirmation', '')
        if confirmation ==  sponsorship.title:
            
            messages.success(request, '贊助已成功刪除')
            Notification.objects.create(
                user=sponsorship.organizer,
                message=f'贊助 "{sponsorship.title}" 已成功刪除'
            )
            sponsorship.delete()
            return redirect('sponsorship_list')  # 或其他適當的頁面
        else:
            messages.error(request, '確認文字不匹配，贊助未被刪除')
    
    return render(request, 'events/delete_sponsorship.html', {'sponsorship': sponsorship})

#處理結案功能
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.exceptions import ValidationError

from .models import Activitynew, Photo  # 確保引入 Photo 模型

@login_required
def toggle_close_activity(request, activity_id):
    activity = get_object_or_404(Activitynew, id=activity_id)

    if request.user == activity.organizer or request.user.is_staff:
        if request.method == "POST":
            activity.is_closed = not activity.is_closed  # 切換結案狀態

            # 如果結案並且有照片上傳
            if activity.is_closed and 'result_photos' in request.FILES:
                photos = request.FILES.getlist('result_photos')  # 獲取所有上傳的文件
                if len(photos) + activity.photos.count() > 20:  # 限制總數最多20張
                    messages.error(request, "照片數量超過限制（最多 20 張）。")
                    return redirect('activity_detail', activity_id=activity.id)

                for photo in photos:
                    # 文件格式驗證
                    if photo.content_type not in ['image/jpeg', 'image/png']:
                        messages.error(request, f"文件 {photo.name} 格式無效，僅支持 JPEG 或 PNG。")
                        continue
                    # 文件大小驗證
                    if photo.size > 5 * 1024 * 1024:  # 限制文件大小為5MB
                        messages.error(request, f"文件 {photo.name} 大小超過 5MB。")
                        continue
                    # 儲存照片到 Photo 模型
                    Photo.objects.create(activity=activity, image=photo)

            activity.save()

            if activity.is_closed:
                messages.success(request, "活動已成功結案，照片已保存！")
            else:
                messages.success(request, "活動結案狀態已取消！")
            return redirect('activity_detail', activity_id=activity.id)

    messages.error(request, "您無權執行此操作。")
    return redirect('activity_detail', activity_id=activity.id)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Activitynew, Photo

@login_required
def edit_activity_photos(request, activity_id):
    activity = get_object_or_404(Activitynew, id=activity_id)

    if request.user != activity.organizer and not request.user.is_staff:
        messages.error(request, "您無權編輯此活動的照片。")
        return redirect('activity_detail', activity_id=activity_id)

    if request.method == "POST":
        # 刪除選中的照片
        photo_ids_to_delete = request.POST.getlist('delete_photos')
        Photo.objects.filter(id__in=photo_ids_to_delete, activity=activity).delete()

        # 上傳新照片
        if 'new_photos' in request.FILES:
            photos = request.FILES.getlist('new_photos')
            if len(photos) + activity.photos.count() > 20:
                messages.error(request, "照片數量超過限制（最多 20 張）。")
            else:
                for photo in photos:
                    if photo.content_type not in ['image/jpeg', 'image/png']:
                        messages.error(request, f"文件 {photo.name} 格式無效，僅支持 JPEG 或 PNG。")
                        continue
                    if photo.size > 5 * 1024 * 1024:
                        messages.error(request, f"文件 {photo.name} 大小超過 5MB。")
                        continue
                    Photo.objects.create(activity=activity, image=photo)

        messages.success(request, "照片已成功更新。")
        return redirect('activity_detail', activity_id=activity_id)

    return render(request, 'events/edit_activity_photos.html', {'activity': activity})

def qa_view(request):
    return render(request, 'events/qa.html')