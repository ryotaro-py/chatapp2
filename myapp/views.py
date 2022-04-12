from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import InquiryForm, LoginForm, MessageForm, UserForm, MailForm, ImgForm
from .models import Message,Member
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required






def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form = InquiryForm()
    params = {'form': form,}
    if request.method == 'POST':
       obj = Member()
       friend_form = InquiryForm(request.POST,request.FILES,instance=obj)
        
       if friend_form.is_valid(): 
                       
            friend_form.save()
            return redirect(to="index")
       else:
            return HttpResponse("a")
    else:
        return render(request, 'myapp/signup.html', params)
      

def login_view(request):
    form = LoginForm()
    params = {'form': form,}
    if request.method == 'POST':
        return render(request, 'myapp/friends.html')
    else:
        return render(request, "myapp/login.html", params)
    

def friends(request):
    others = Member.objects.all().exclude(pk=request.user.pk)
    l=[]
    for other in others:
        message_other = other.message_owner.all().filter(friend=request.user)
        message_user = other.message_friend.all().filter(owner=request.user)
        message__other = message_other.first()
        message__user = message_user.first()
        print(message__user)
        if message__other == None and message__user == None:
            m = ''
        elif message__other == None:
            m = message__user
        elif message__user == None:
            m = message__other
        elif message__other.date > message__user.date:
            message = message__other.values()
            m = message
        else:
            message = message__user.message.values()
            m = message
        l.append([other, m])
        
    params = {
         'l': l, 
    }
    return render(request, "myapp/friends.html", params)
    

def talk_room(request, pk):
    other = Member.objects.get(pk=pk)
    user = request.user
    message = Message.objects.all().filter(
       Q(Q(friend=request.user), Q(owner=other))|
       Q(Q(friend=other), Q(owner=request.user))
    ).order_by('-date')
    # message=Message.objects.filter(Q(friend=request.user)|Q(friend=other)).filter(Q(owner=request.user)|Q(owner=other))
    form = MessageForm()
    params = {
        'other': other,
        'user' : user,
        'message': message,
        'form':form,
        'pk':pk,
    }
    if request.method == 'POST':
        obj = Message(friend=other,owner=request.user)
        message = MessageForm(request.POST, instance=obj)
        if message.is_valid():
            message.save()       
    return render(request, "myapp/talk_room.html", params)

    
def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def user(request):
    form=UserForm()
    user=request.user
    obj = request.user
    if request.method == 'POST':
        print("aaa")
        name = UserForm(request.POST,instance=obj)
        print(request.POST)
        print(name)
        if name.is_valid():
            name.save()
            return redirect(to="userdone")
    return render(request, 'myapp/user.html', {'form':form })


def userdone(request):
    return render(request, 'myapp/userdone.html')

@login_required
def mail(request):
    obj = Member.objects.get(pk=request.user.pk)
    form = MailForm(instance=obj)
    if request.method == 'POST':
        mail = MailForm(request.POST, instance=obj)
        mail.save()
    return render(request, 'myapp/mail.html', {'form': form})

def maildone(request):
    return render(request, 'myapp/maildone.html')

@login_required
def img(request):
    obj = Member.objects.get(pk=request.user.pk)
    form = ImgForm(instance=obj)
    if request.method == 'POST':
        img = ImgForm(request.POST, instance=obj)
        img.save()
    return render(request, 'myapp/img.html', {'form':form})

def imgdone(request):
    return render(request, 'myapp/imgdone.html')

@login_required
def password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(to='password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'myapp/password.html', {'form': form})

def passworddone(request):
    return render(request, 'myapp/passworddone.html')

@login_required
def logout_view(request):
   logout(request)
   return render(request, 'myapp/index.html')





    
        