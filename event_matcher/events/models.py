from django.db import models
from django.contrib.auth.models import User


#設計「活動」模型（Activity Model）
class Activity(models.Model):
    title = models.CharField(max_length=200)           # 活動名稱
    description = models.TextField()                   # 活動描述
    location = models.CharField(max_length=100)        # 活動地點
    date = models.DateField()                          # 活動日期
    image = models.ImageField(upload_to='activity_images/', blank=True, null=True)  # 活動圖片
    is_favorited = models.BooleanField(default=False)  # 收藏狀態

    def __str__(self):
        return self.title
    
# 設計「贊助」模型（Sponsorship Model）
class Sponsorship(models.Model):
    title = models.CharField(max_length=200)            # 贊助名稱
    description = models.TextField()                    # 贊助描述
    sponsor = models.CharField(max_length=100)          # 贊助者名稱
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # 贊助金額
    image = models.ImageField(upload_to='sponsorship_images/', blank=True, null=True)  # 贊助圖片
    location = models.CharField(max_length=100,default="unknown")        # 贊助地點
    date_posted = models.DateField(auto_now_add=True)   # 贊助發布日期
    is_favorited = models.BooleanField(default=False)   # 收藏狀態

    def __str__(self):
        return self.title



# Create your models here.
