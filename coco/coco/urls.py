"""
URL configuration for coco project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
import mainsite.views as mainsite

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", mainsite.homepage),
    path("activity/", mainsite.activity),
    path("activity/create/", mainsite.create_activity),
    path("company/", mainsite.company),
    path("company/create/", mainsite.create_company),
    path('login/', mainsite.login),
    path('logout/', mainsite.logout),
    path('userinfo/', mainsite.userinfo),
    path('register/', mainsite.register),
    re_path(r'^captcha/', include('captcha.urls')),
]
