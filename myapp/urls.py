from django.urls import path
from . import views
from django.conf.urls import include


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup', views.SignupView.as_view(), name='signup_view'),
    path('login', views.LoginView.as_view(), name='login_view'),
    path('friends', views.FriendView.as_view(), name='friends'),
    path('talk_room/<int:pk>', views.TalkRoomView.as_view(), name='talk_room'),
    path('setting', views.SettingView.as_view(), name='setting'),
    path('user', views.UserView.as_view(), name='user'),
    path('userdone', views.UserdoneView.as_view(), name='userdone'),
    path('mail', views.MailView.as_view(), name='mail'),
    path('maildone', views.MaildoneView.as_view(), name='maildone'),
    path('img', views.ImgView.as_view(), name='img'),
    path('imgdone', views.ImgdoneView.as_view(), name='imgdone'),
    path('password_view', views.PasswordView.as_view(), name='password_view'),
    path('passworddone', views.PassworddoneView.as_view(), name='passworddone'),
    path('logout', views.LogoutView.as_view(), name='logout'),
]



