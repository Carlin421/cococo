from django.urls import path
from . import views
#將活動列表和收藏功能連結起來。
urlpatterns = [
    path('', views.activity_list, name='activity_list'),  # 使用 activity_list
    path('toggle_activity_favorite/<int:event_id>/', views.toggle_activity_favorite, name='toggle_activity_favorite'),
    path('toggle_sponsorship_favorite/<int:sponsorship_id>/', views.toggle_sponsorship_favorite, name='toggle_sponsorship_favorite'),
]

