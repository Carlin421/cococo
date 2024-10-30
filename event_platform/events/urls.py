from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('find-events/', views.find_events, name='find_events'),  # 找活動
    path('find-sponsorships/', views.find_sponsorships, name='find_sponsorships'),  # 找贊助
    path('login/', views.user_login, name='login'),  # 登入頁面
    path('logout/', views.user_logout, name='logout'),  # 登出路由
    path('register/', views.register, name='register'),  # 註冊頁面

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]