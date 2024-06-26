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
    path('register_content_creator/', views.register_content_creator, name='register_content_creator'),

    path('', views.loginnew, name='loginnew'),
    path('normal_user_home/', views.normal_user_home, name='normal_user_home'),
    path('college_user_home/', views.college_user_home, name='college_user_home'),
    path('content_creator_home/', views.content_creator_home, name='content_creator_home'),
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
    path('update_profile_content_creators/', views.update_profile_content_creators, name='update_profile_content_creators'),
    path('news',views.news,name='news'),
    path('profile/',views.profile,name='profile'),
    path('profile2/',views.profile2,name='profile2'),
    path('creatorprofile/',views.creatorprofile,name='creatorprofile'),
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
    path('course/<int:course_id>/add_modulesnew/', views.add_modulesnew, name='add_modulesnew'),

    path('course/<int:course_id>/add_chapters/', views.add_chapters, name='add_chapters'),
    path('course/<int:course_id>/add_chaptersnew/', views.add_chaptersnew, name='add_chaptersnew'),

    path('course/<int:course_id>/add_material/', views.add_course_material, name='add_course_material'),
    path('course/<int:course_id>/add_materialnew/', views.add_course_materialnew, name='add_course_materialnew'),
    path('ajax/get_chapters_for_module/<int:module_id>/', views.get_chapters_for_module, name='get_chapters_for_module'),

    path('course_list/', views.course_list, name='course_list'), 
    path('course_list_college/', views.course_list_college, name='course_list_college'),

    path('course/<int:course_id>/', views.course_detail, name='course_detail'),

    path('course_creator/<int:course_id>/', views.course_detail_creator, name='course_detail_creator'),

    path('course_detail_user/<int:course_id>/', views.course_detail_user, name='course_detail_user'),
    path('enrolled_course_detail_user/<int:course_id>/', views.enrolled_course_details, name='enrolled_course_details'),

    path('chapter/<int:chapter_id>/', views.chapter_detail, name='chapter_details'),
    path('toggle_user_activation/<int:user_id>/', views.toggle_user_activation, name='toggle_user_activation'),

    path('courses/<int:course_id>/', views.course_detail_view, name='course_detail_view'),
    #path('course/enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),
    path('get_chapter_content/<int:chapter_id>/', views.get_chapter_content, name='get_chapter_content'),
    path('courses/<int:course_id>/progress/', views.course_progress, name='course_progress'),
    path('update_progress/', views.update_progress, name='update_progress'),
    path('posts/', views.post_list_and_create, name='post_list_and_create'),
    path('posts_new/', views.post_list_and_create_new, name='post_list_and_create_new'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('like_post/', views.like_post, name='like_post'),
    path('save_post/', views.save_post, name='save_post'),
    path('saved-posts/', views.view_saved_posts, name='view_saved_posts'),
    path('hashtag/<str:hashtag>/', views.posts_by_hashtag, name='posts_by_hashtag'),
    path('hashtag/<str:hashtag>/', views.posts_by_hashtagg, name='posts_by_hashtagg'),
    path('courses/<int:course_id>/download_certificate/', views.download_certificate, name='download_certificate'),
    path('enrolled-courses/', views.enrolled_courses_view, name='enrolled_courses'),
    path('upload/', views.transcribe_audio, name='transcribe_audio'),
    path('get-random-content/', views.get_random_content, name='get_random_content'),
    path('upload/', views.upload, name='upload'),

    path('add_course_by_creator',views.add_course_by_creator,name='add_course_by_creator'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('community/create/<int:course_id>/', views.create_community, name='create_community'),
    path('communities/', views.community_detail, name='community_detail'),
    path('communities/user/', views.community_detailsnew, name='community_detail_user'),
    path('community/chat/<int:community_id>/', views.community_chat, name='community_chat'),
    path('community/chat_user/<int:community_id>/', views.community_chat_user, name='community_chat_user'),
    path('code-editor/', views.code_editor, name='code_editor'),
    path('add-book/', views.add_book, name='add_book'),
    path('view-book/<int:book_id>/', views.view_book, name='view_book'),


    #restframework
    path('api/register/', views.register_normaluser_flutter, name='register_normaluser_flutter'),
    path('api/mobile/login/', views.mobile_login, name='mobile_login'),
    path('api/user/profile/', views.get_user_profile, name='user_profile'),

    path('college_dashboard/', views.college_dashboard, name='college_dashboard'),
    path('content_creator_dashboard/', views.content_creator_dashboard, name='content_creator_dashboard'),
    path('api/courses/', views.course_list_new, name='course-list'),
    path('api/enrollments/', views.get_user_enrollments, name='user-enrollments'),
    path('api/profile/update/', views.update_profile_new, name='update_profile_new'),
    path('api/courseslist/', views.course_list_create, name='course-list-create'),
    path('api/coursesnew/<int:pk>/', views.course_detail, name='course-detail'),
    path('api/posts/', views.list_posts, name='list-posts'),


    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)