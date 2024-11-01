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
    path('find_activity/', views.activitynew_list, name='activitynew_list'),
    path('toggle_activitynew_favorite/<int:activity_id>/', views.toggle_activitynew_favorite, name='toggle_activitynew_favorite'),
    path('find_sponsorship/', views.sponsorship_list, name='sponsorship_list'),
    path('toggle_sponsorshipnew_favorite/<int:sponsorship_id>/', views.toggle_sponsorshipnew_favorite, name='toggle_sponsorshipnew_favorite'),
    path('', views.activity_list, name='event_list'),
]
