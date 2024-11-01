from django.urls import path, include
from . import views
from .views import login_view, register_view
from django.contrib.auth.views import LogoutView

# 將活動列表和收藏功能連結起來
urlpatterns = [
    path('toggle_activity_favorite/<int:event_id>/', views.toggle_activity_favorite, name='toggle_activity_favorite'),
    path('toggle_sponsorship_favorite/<int:sponsorship_id>/', views.toggle_sponsorship_favorite, name='toggle_sponsorship_favorite'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('logout/', LogoutView.as_view(next_page='activity_list'), name='logout'),  # 登出並重導向
    path('', views.activity_list, name='event_list'),
]
