from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

    
#設計「主活動」模型（Activitynew Model）
class Activitynew(models.Model):
    title = models.CharField(max_length=200)           # 活動名稱
    description = models.TextField()                   # 活動描述
    location = models.CharField(max_length=100)        # 活動地點
    date = models.DateField()                          # 活動日期
    image = models.ImageField(upload_to='activitynew_images/', blank=True, null=True)  # 活動圖片
    is_favorited = models.BooleanField(default=False)  # 收藏狀態
    check_status = models.BooleanField(default=False) # 審核狀態

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




# Create your models here.
