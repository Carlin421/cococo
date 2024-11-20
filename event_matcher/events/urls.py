from django.urls import path, include
from . import views
from .views import login_view, register_view, custom_logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('toggle_activity_favorite/<int:event_id>/', views.toggle_activity_favorite, name='toggle_activity_favorite'),
    path('toggle_sponsorship_favorite/<int:sponsorship_id>/', views.toggle_sponsorship_favorite, name='toggle_sponsorship_favorite'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('logout/', custom_logout, name='logout'),
    path('find_activity/', views.activitynew_list, name='activitynew_list'),
    # path('toggle_activitynew_favorite/<int:activity_id>/', views.toggle_activitynew_favorite, name='toggle_activitynew_favorite'),
    path('find_sponsorship/', views.sponsorship_list, name='sponsorship_list'),
    # path('toggle_sponsorshipnew_favorite/<int:sponsorship_id>/', views.toggle_sponsorshipnew_favorite, name='toggle_sponsorshipnew_favorite'),
    path('', views.activity_list, name='event_list'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='events/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='events/password_change_done.html'), name='password_change_done'),
    path('activity/<int:activity_id>/', views.activity_detail, name='activity_detail'),
    path('sponsorship_list/', views.sponsorship_list, name='sponsorship_list'),
    path('activities/', views.activitynew_list, name='activitynew_list'),
    path('about/', views.about_us, name='about_us'),
    path('add_activity/', views.add_activity, name='add_activity'),
    path('add_sponsorship/', views.add_sponsorship, name='add_sponsorship'),
    path('sponsor/<int:sponsorship_id>/', views.sponsor_detail, name='sponsor_detail'),
    path('sponsorship_list/', views.sponsorship_list, name='sponsorship_list'),
    path('sponsorship_list/<int:page>/', views.sponsorship_list, name='sponsorship_list_page'),
    path('check_activity/',views.check_activity, name = 'check_activity'),
    path('check_sponsorship/',views.check_sponsorship, name = 'check_sponsorship'),
    path('toggle_activity_check/<int:event_id>/',views.toggle_activity_check, name = 'toggle_activity_check'),
    path('toggle_sponsorship_check/<int:event_id>/',views.toggle_sponsorship_check, name = 'toggle_sponsorship_check'),
    path('chatbot/', views.chatbot_view, name='chatbot'),

]

