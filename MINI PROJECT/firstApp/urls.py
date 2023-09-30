from . import views
from django.urls import path

urlpatterns = [
    path('',views.registernew,name='registernew'),
    path('home',views.home,name='home'),
    path('login_view',views.login_view,name='login_view'),
    path('logoutp',views.logoutp,name='logoutp'),
]
