from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        unread_count = notifications.filter(is_read=False).count()
        return {
            'notifications': notifications[:5],  # 只在這裡進行切片
            'unread_notifications_count': unread_count
        }
    return {}