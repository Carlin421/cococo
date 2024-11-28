from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

#11/19 這塊還未使用在任何介面
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True,default='user_photos/default.jpg')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

#設計「主活動」模型（Activitynew Model）
class Activitynew(models.Model):
    title = models.CharField(max_length=200)           # 活動名稱
    description = models.TextField()                   # 活動描述
    location = models.CharField(max_length=255, verbose_name="活動地點")
    latitude = models.FloatField(null=True, blank=True, verbose_name="緯度")
    longitude = models.FloatField(null=True, blank=True, verbose_name="經度")
    date = models.DateField()                          # 活動日期
    image = models.ImageField(upload_to='activitynew_images/', blank=True, null=True)  # 活動圖片
    is_favorited = models.BooleanField(default=False)  # 收藏狀態
    check_status = models.BooleanField(default=False) # 審核狀態
    is_active = models.BooleanField(default=True)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_activities',
        null=True,
        blank=True
    )
    def __str__(self):
        return self.title
    
# 設計「主贊助」模型（Sponsorship Model）
class Sponsorshipnew(models.Model):
    title = models.CharField(max_length=200)            # 贊助名稱
    description = models.TextField()                    # 贊助描述
    sponsor = models.CharField(max_length=100)          # 贊助者名稱
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # 贊助金額
    image = models.ImageField(upload_to='sponsorship_images/', blank=True, null=True)  # 贊助圖片
    location = models.CharField(max_length=100,default="unknown")        # 贊助地點
    date_posted = models.DateTimeField(default=timezone.now)  # 贊助發布日期
    is_favorited = models.BooleanField(default=False)   # 收藏狀態
    check_status = models.BooleanField(default=False) # 審核狀態
    is_active = models.BooleanField(default=True)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_sponsorships',  
        null=True,
        blank=True
    )
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    activity = models.ForeignKey('Activitynew', on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.message}"
# Create your models here.
