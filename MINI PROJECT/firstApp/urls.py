from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('home/', views.home, name='home'),
    path('register_normal_user/', views.register_normal_user, name='register_normal_user'),
    path('register_college_user/', views.register_college_user, name='register_college_user'),
    path('', views.loginnew, name='loginnew'),
    path('normal_user_home/', views.normal_user_home, name='normal_user_home'),
    path('college_user_home/', views.college_user_home, name='college_user_home'),
    path('logoutnew/', views.logoutnew, name='logoutnew'),
    path('your_view/', views.your_view, name='your_view'),
    path('logoutp/', views.logoutp, name='logoutp'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

