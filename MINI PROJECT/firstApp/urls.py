from . import views
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('home',views.home,name='home'),
    path('logoutp',views.logoutp,name='logoutp'),

    path('register/normal/', views.register_normal_user, name='register_normal_user'),
    path('register/college/', views.register_college_user, name='register_college_user'),
    path('', views.loginnew, name='loginnew'),
    path('college_user_home/', views.college_user_home, name='college_user_home'),
    path('normal_user_home/', views.normal_user_home, name='normal_user_home'),
    path('logoutnew',views.logoutnew,name='logoutnew'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
