from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponse
from .forms import InquiryForm, LoginForm, MessageForm, UserForm, MailForm, ImgForm
from .models import Member, Message
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin



# def index(request):
#     return render(request, "myapp/index.html")

class IndexView(generic.TemplateView):
    template_name = "myapp/index.html"

# def signup_view(request):
#     form = InquiryForm()
#     params = {'form': form,}
#     if request.method == 'POST':
#        obj = Member()
#        friend_form = InquiryForm(request.POST,request.FILES,instance=obj)
        
#        if friend_form.is_valid(): 
                       
#             friend_form.save()
#             return redirect(to="index")
#        else:
#             return HttpResponse("a")
#     else:
#         return render(request, 'myapp/signup.html', params)

class SignupView(generic.FormView):
    template_name = "myapp/signup.html"
    form_class = InquiryForm
    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=Member())
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            params = {
                'form' : form,
                'message' : 'Enter a valid email addres.\n The two password fields didn''t match. ' 
            }
            return render(request, self.template_name, params)
        return render(request, self.template_name, {'form': form,})

     

# def login_view(request):
#     form = LoginForm()
#     params = {'form': form,}
#     if request.method == 'POST':
#         return render(request, 'myapp/friends.html')
#     else:
#         return render(request, "myapp/login.html", params)

class LoginView(generic.FormView):
    template_name = "myapp/login.html"
    form_class = LoginForm
    def post(self):
        return redirect('friends')
    

def friends(request):
    others = Member.objects.all().exclude(pk=request.user.pk)
    l=[]
    for other in others:
        message_other = other.message_owner.all().filter(friend=request.user)
        message_user = other.message_friend.all().filter(owner=request.user)
        message__other = message_other.first()
        message__user = message_user.first()
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


class FriendView(LoginRequiredMixin, generic.ListView):
    template_name = "myapp/friends.html"
    

    def get_queryset(self):
        queryset = Member.objects.all().exclude(pk=self.request.user.pk)
        query = self.request.GET.get('query')
        print(query)
        if query:
            queryset = queryset.filter(username__icontains=query)
        return queryset


   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        others = Member.objects.all().exclude(pk=self.request.user.pk)
        context["message"]=[]
        query = self.request.GET.get('query')
        if query:
            others = others.filter(username__icontains=query)
        for other in others:            
            message = Message.objects.all().filter(
                Q(Q(owner=self.request.user),Q(friend=other))|
                Q(Q(friend=self.request.user),Q(owner=other))
            ).order_by('-date').first()
            context["message"].append([other, message])
        return context

    
    
        

    

# def talk_room(request, pk):
#     other = Member.objects.get(pk=pk)
#     user = request.user
#     message = Message.objects.all().filter(
#        Q(Q(friend=request.user), Q(owner=other))|
#        Q(Q(friend=other), Q(owner=request.user))
#     ).order_by('-date')
#     # message=Message.objects.filter(Q(friend=request.user)|Q(friend=other)).filter(Q(owner=request.user)|Q(owner=other))
#     form = MessageForm()
#     params = {
#         'other': other,
#         'user' : user,
#         'message': message,
#         'form':form,
#         'pk':pk,
#     }
#     if request.method == 'POST':
#         obj = Message(friend=other,owner=request.user)
#         message = MessageForm(request.POST, instance=obj)
#         if message.is_valid():
#             message.save()       
#     return render(request, "myapp/talk_room.html", params)

class TalkRoomView(LoginRequiredMixin, generic.FormView):
    template_name = "myapp/talk_room.html"
    form_class = MessageForm
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        other = Member.objects.get(pk=self.kwargs['pk'])
        context['other'] = other
        context['message'] = Message.objects.all().filter(
            Q(Q(friend=self.request.user), Q(owner=other))|
            Q(Q(friend=other), Q(owner=self.request.user))
        ).order_by('-date')
        context['user'] = self.request.user
        context['pk'] = self.kwargs['pk']
        return context
        
    def post(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        other = Member.objects.get(pk=self.kwargs['pk'])
        context['other'] = other
        context['message'] = Message.objects.all().filter(
            Q(Q(friend=self.request.user), Q(owner=other))|
            Q(Q(friend=other), Q(owner=self.request.user))
        ).order_by('-date')
        context['user'] = self.request.user
        context['pk'] = self.kwargs['pk']
        form = self.form_class(request.POST)
        obj = Message(friend=other, owner=self.request.user)
        message = MessageForm(request.POST, instance=obj)
        if message.is_valid():
            message.save()
        # return redirect('talk_room', kwargs={'pk': self.kwargs['pk']})
        # return reverse_lazy('talk_room', kwargs={'pk': self.kwargs['pk']})
        return render(request, self.template_name, 
        {'form':self.form_class,
        'other':context['other'],
        'message':context['message'],
        'user': context['user'],}) 

    def get_success_url(self):
        return reverse_lazy('talk_room', kwargs={'pk': self.kwargs['pk']})
        


    
# def setting(request):
#     return render(request, "myapp/setting.html")

class SettingView(LoginRequiredMixin, generic.TemplateView):
    template_name = "myapp/setting.html"
    


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

class UserView(LoginRequiredMixin, generic.FormView):
    template_name = "myapp/user.html"
    form_class = UserForm

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            name.save()
            return redirect(to='userdone')
        return render(request, self.template_name, {"form": form})


def userdone(request):
    return render(request, 'myapp/userdone.html')

class UserdoneView(generic.TemplateView):
    template_name = 'myapp/userdone.html'

@login_required
def mail(request):
    obj = Member.objects.get(pk=request.user.pk)
    form = MailForm(instance=obj)
    if request.method == 'POST':
        mail = MailForm(request.POST, instance=obj)
        mail.save()
    return render(request, 'myapp/mail.html', {'form': form})

class MailView(LoginRequiredMixin, generic.FormView):
    template_name = 'myapp/mail.html'

    def get(self, request):
        obj = Member.objects.get(pk=request.user.pk)
        form = MailForm(instance=obj)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        obj = Member.objects.get(pk=request.user.pk)
        form = MailForm(instance=obj)
        mail = MailForm(request.POST, instance=obj)
        if mail.is_valid():
            mail.save()
            return redirect(to='maildone')
        return render(request, self.template_name, {'form': form})


def maildone(request):
    return render(request, 'myapp/maildone.html')

class MaildoneView(generic.TemplateView):
    template_name = 'myapp/maildone.html'

@login_required
def img(request):
    obj = Member.objects.get(pk=request.user.pk)
    form = ImgForm(instance=obj)
    if request.method == 'POST':
        img = ImgForm(request.POST, instance=obj)
        img.save()
    return render(request, 'myapp/img.html', {'form':form})

class ImgView(LoginRequiredMixin, generic.FormView):
    template_name = 'myapp/img.html'

    def get(self, request):
        obj = Member.objects.get(pk=request.user.pk)
        form = ImgForm(instance=obj)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        obj = Member.objects.get(pk=request.user.pk)
        form = ImgForm(instance=obj)
        img = ImgForm(request.POST, instance=obj)
        if img.is_valid():
            img.save()
            return redirect(to='imgdone')
        return render(request, self.template_name, {'form': form})
        

def imgdone(request):
     return render(request, 'myapp/imgdone.html')

class ImgdoneView(generic.TemplateView):
    template_name = 'myapp/imgdone.html'
     
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

class PasswordView(LoginRequiredMixin, generic.FormView):
    template_name = 'myapp/password.html'

    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(to='password')
        return render(request, self.template_name, {'form':form})

def passworddone(request):
    return render(request, 'myapp/passworddone.html')

class PassworddoneView(generic.TemplateView):
    template_name = 'myapp/passworddone.html'

# @login_required
# def logout_view(request):
#     logout(request)
#     return render(request, 'myapp/index.html')

class LogoutView(LogoutView):
    success_url = reverse_lazy('myapp/index.html')






    
        