from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('home/', views.home, name='home'),
    path('home2/', views.home2, name='home2'),
    path('register_normal_user/', views.register_normal_user, name='register_normal_user'),
    path('register_college_user/', views.register_college_user, name='register_college_user'),
    path('', views.loginnew, name='loginnew'),
    path('normal_user_home/', views.normal_user_home, name='normal_user_home'),
    path('college_user_home/', views.college_user_home, name='college_user_home'),
    #path('logoutnew/', views.logoutnew, name='logoutnew'),
    path('your_view/', views.your_view, name='your_view'),
    path('logoutp/', views.logoutp, name='logoutp'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('news',views.news,name='news'),
    path('profile/',views.profile,name='profile'),
    path('department',views.add_department,name='department'),
    path('add_course',views.add_course,name='add_course'),

    path('update_profile/', views.update_profile, name='update_profile'),
    path('model_update_profile/', views.model_update_profile, name='model_update_profile'),

    path('viewprofile/', views.view_profile, name='viewprofile'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),

    path('college_details/<int:pk>/', views.college_details, name='college_details'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),
    path('add_instructor/', views.add_instructor, name='add_instructor'),
    path('get_instructors_for_department/<int:department_id>/', views.get_instructors_for_department, name='get_instructors_for_department'),
    path('view_instructors',views.view_instructors,name='view_instructors'),

    



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)