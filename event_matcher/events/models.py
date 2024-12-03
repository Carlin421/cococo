from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True,default='user_photos/default.jpg')
    description = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=[('brand', '品牌方'), ('club', '社團方')], blank=True)
    @property
    def is_brand(self):
        return self.role == 'brand'

    @property
    def is_club(self):
        return self.role == 'club'
    def __str__(self):
        return f"{self.user.username}'s profile"

#設計「主活動」模型（Activitynew Model）
class Activitynew(models.Model):
    title = models.CharField(max_length=200)           # 活動名稱
    description = models.TextField()                   # 活動描述
    max_participants = models.IntegerField(null=True, blank=True)   #參與人數上限
    current_participants = models.IntegerField(null=True, blank=True)   #目前報名人數
    location = models.CharField(max_length=255, verbose_name="活動地點")
    latitude = models.FloatField(null=True, blank=True, verbose_name="緯度")
    longitude = models.FloatField(null=True, blank=True, verbose_name="經度")
    date = models.DateField()                          # 活動日期
    registration_deadline = models.DateField(null=True, blank=True) #活動截止日期
    image = models.ImageField(upload_to='activitynew_images/', blank=True, null=True,default=None)  # 活動圖片
    date_posted = models.DateTimeField(default=timezone.now)  # 活動發布日期
    check_status = models.BooleanField(default=False) # 審核狀態
    is_closed = models.BooleanField(default=False)  # 用於標記活動是否已結案
    result_photo = models.ImageField(upload_to='result_photos/', blank=True, null=True,default=None)
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
    item = models.CharField(max_length=100,default=" ") #贊助商品
    people = models.TextField(max_length=100,default=" ") #宣傳模式
    amount = models.DecimalField(
    max_digits=10, 
    decimal_places=2, 
    validators=[MinValueValidator(0)]  # 0作最小值
)  # 贊助金額
    image = models.ImageField(upload_to='sponsorship_images/', blank=True, null=True)  # 贊助圖片
    location = models.CharField(max_length=100,default=" ")        # 贊助地點
    date_posted = models.DateTimeField(default=timezone.now)  # 贊助發布日期
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
    activity = models.ForeignKey('Activitynew', on_delete=models.CASCADE, null=True, blank=True)
    sponsorship = models.ForeignKey('Sponsorshipnew', on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.message}"
# Create your models here.
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    activity = models.ForeignKey('Activitynew', on_delete=models.CASCADE, null=True, blank=True)
    sponsorship = models.ForeignKey('Sponsorshipnew', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'activity'], ['user', 'sponsorship']]

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.activity or self.sponsorship}"

from django import forms

class CloseActivityForm(forms.ModelForm):
    class Meta:
        model = Activitynew
        fields = ['result_photo']

class Photo(models.Model):
    activity = models.ForeignKey(Activitynew, related_name="photos", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="activity_photos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)