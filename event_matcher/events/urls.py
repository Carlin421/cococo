from django.urls import path
from . import views
from .views import login_view, register_view
from django.urls import include, path

#將活動列表和收藏功能連結起來。
urlpatterns = [
    path('', views.activity_list, name='activity_list'),  # 使用 activity_list
    path('toggle_activity_favorite/<int:event_id>/', views.toggle_activity_favorite, name='toggle_activity_favorite'),
    path('toggle_sponsorship_favorite/<int:sponsorship_id>/', views.toggle_sponsorship_favorite, name='toggle_sponsorship_favorite'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    # events/urls.py
    path('', views.activity_list, name='event_list'),


]

