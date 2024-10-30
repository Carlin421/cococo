from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/')
    attendees = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('品牌', '品牌身份'),
        ('社團', '社團身份'),
    ]
    
    # 將 email 欄位設為必填且不可為空
    email = models.EmailField(unique=True)  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f'{self.user.username} ({self.user_type})'


# Create your models here.
