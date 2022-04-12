from django.urls import path
from . import views
from django.conf.urls import include


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:pk>/', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('user', views.user, name='user'),
    path('userdone', views.userdone, name='userdone'),
    path('mail', views.mail, name='mail'),
    path('maildone', views.maildone, name='maildone'),
    path('img', views.img, name='img'),
    path('imgdone', views.imgdone, name='imgdone'),
    path('password_view', views.password_view, name='password_view'),
    path('passworddone', views.passworddone, name='passworddone'),
    path('logout', views.logout_view, name='logout_view'),
]



