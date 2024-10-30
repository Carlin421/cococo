from django.contrib import admin
from .models import Event

admin.site.register(Event)

from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email','user_type')
    list_filter = ('user_type',)  # 根據會員身份篩選

admin.site.register(Profile, ProfileAdmin)



# Register your models here.
