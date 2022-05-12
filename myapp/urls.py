from django.urls import path
from . import views
from django.conf.urls import include


urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    # path('signup', views.signup_view, name='signup_view'),
    path('signup', views.SignupView.as_view(), name='signup_view'),
    # path('login', views.login_view, name='login_view'),
    path('login', views.LoginView.as_view(), name='login_view'),
    # path('friends', views.friends, name='friends'),
    path('friends', views.FriendView.as_view(), name='friends'),
    #path('talk_room/<int:pk>/', views.talk_room, name='talk_room'),
    path('talk_room/<int:pk>', views.TalkRoomView.as_view(), name='talk_room'),
    #path('setting', views.setting, name='setting'),
    path('setting', views.SettingView.as_view(), name='setting'),
    # path('user', views.user, name='user'),
    path('user', views.UserView.as_view(), name='user'),
    # path('userdone', views.userdone, name='userdone'),
    path('userdone', views.UserdoneView.as_view(), name='userdone'),
    # path('mail', views.mail, name='mail'),
    path('mail', views.MailView.as_view(), name='mail'),
    # path('maildone', views.maildone, name='maildone'),
    path('maildone', views.MaildoneView.as_view(), name='maildone'),
    # path('img', views.img, name='img'),
    path('img', views.ImgView.as_view(), name='img'),
    # path('imgdone', views.imgdone, name='imgdone'),
    path('imgdone', views.ImgdoneView.as_view(), name='imgdone'),
    # path('password_view', views.password_view, name='password_view'),
    path('password_view', views.PasswordView.as_view(), name='password_view'),
    # path('passworddone', views.passworddone, name='passworddone'),
    path('passworddone', views.PassworddoneView.as_view(), name='passworddone'),
    # path('logout', views.logout_view, name='logout_view'),
    path('logout', views.LogoutView.as_view(), name='logout'),
]



