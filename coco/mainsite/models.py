from django.db import models

# Create your models here.
class ActivityPost(models.Model):
    title = models.CharField(max_length=100)#活動標題
    content = models.TextField()#活動內容
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
class CompanyPost(models.Model):
    title = models.CharField(max_length=100)#公司標題
    content = models.TextField()#公司內容
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class User(models.Model):
    name = models.CharField(max_length=20, default = False)
    email = models.EmailField()
    password = models.CharField(max_length=20 , null = False)
    enabled = models.BooleanField(default = False)
    def __str__(self):
        return self.name