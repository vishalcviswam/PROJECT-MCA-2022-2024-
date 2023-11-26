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
    path('admin_home/', views.admin_home, name='admin_home'),
    #path('logoutnew/', views.logoutnew, name='logoutnew'),
    path('your_view/', views.your_view, name='your_view'),
    path('logoutp/', views.logoutp, name='logoutp'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('college_update_profile/', views.update_college_profile, name='update_college_profile'),
    path('news',views.news,name='news'),
    path('profile/',views.profile,name='profile'),
    path('profile2/',views.profile2,name='profile2'),
    path('department',views.add_department,name='department'),
    path('add_course',views.add_course,name='add_course'),

    path('update_profile/', views.update_profile, name='update_profile'),
    path('model_update_profile/', views.model_update_profile, name='model_update_profile'),

    path('viewprofile/', views.view_profile, name='viewprofile'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),

    path('college_details/<int:pk>/', views.college_details, name='college_details'),
    path('deactivate_department/<int:department_id>/', views.deactivate_department, name='deactivate_department'),
    path('add_instructor/', views.add_instructor, name='add_instructor'),
    path('get_instructors_for_department/<int:department_id>/', views.get_instructors_for_department, name='get_instructors_for_department'),
    path('view_instructors',views.view_instructors,name='view_instructors'),
    path('course/<int:course_id>/add_modules/', views.add_modules, name='add_modules'),
    path('course/<int:course_id>/add_chapters/', views.add_chapters, name='add_chapters'),
    path('course/<int:course_id>/add_material/', views.add_course_material, name='add_course_material'),
    path('ajax/get_chapters_for_module/<int:module_id>/', views.get_chapters_for_module, name='get_chapters_for_module'),

    path('course_list/', views.course_list, name='course_list'), 
    path('course_list_college/', views.course_list_college, name='course_list_college'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course_detail_user/<int:course_id>/', views.course_detail_user, name='course_detail_user'),
    path('chapter/<int:chapter_id>/', views.chapter_detail, name='chapter_details'),
    path('toggle_user_activation/<int:user_id>/', views.toggle_user_activation, name='toggle_user_activation'),

    path('courses/<int:course_id>/', views.course_detail_view, name='course_detail_view'),
    path('course/enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),
    path('get_chapter_content/<int:chapter_id>/', views.get_chapter_content, name='get_chapter_content'),
    path('courses/<int:course_id>/progress/', views.course_progress, name='course_progress'),
    path('update_progress/', views.update_progress, name='update_progress'),
    path('posts/', views.post_list_and_create, name='post_list_and_create'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('like_post/', views.like_post, name='like_post'),
    path('save_post/', views.save_post, name='save_post'),
    path('saved-posts/', views.view_saved_posts, name='view_saved_posts'),
    path('hashtag/<str:hashtag>/', views.posts_by_hashtag, name='posts_by_hashtag'),
    path('hashtag/<str:hashtag>/', views.posts_by_hashtagg, name='posts_by_hashtagg'),
    path('courses/<int:course_id>/download_certificate/', views.download_certificate, name='download_certificate'),


    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)