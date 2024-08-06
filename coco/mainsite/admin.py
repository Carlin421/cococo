from django.contrib import admin
from .models import ActivityPost, CompanyPost, User
# Register your models here.

admin.site.register(ActivityPost)
admin.site.register(CompanyPost)
admin.site.register(User)