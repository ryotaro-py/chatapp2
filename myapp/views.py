from email import message
from multiprocessing import context
from django.dispatch import receiver
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





class IndexView(generic.TemplateView):
    template_name = "myapp/index.html"



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
        

     



class LoginView(generic.FormView):
    template_name = "myapp/login.html"
    form_class = LoginForm
    def post(self):
        return redirect('friends')
    
from django.db.models import Max, F, Case, When
from django.db.models.functions import Coalesce, Greatest

class FriendView(LoginRequiredMixin, generic.ListView):
    template_name = "myapp/friends.html"
    

    def get_queryset(self):
        queryset = Member.objects.all().exclude(pk=self.request.user.pk)
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(username__icontains=query)
        return queryset


   
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     others = Member.objects.all().exclude(pk=self.request.user.pk)
    #     context["message"]=[]
    #     query = self.request.GET.get('query')
    #     if query:
    #         others = others.filter(username__icontains=query)
    #     for other in others:            
    #         message = Message.objects.all().filter(
    #             Q(Q(owner=self.request.user),Q(friend=other))|
    #             Q(Q(friend=self.request.user),Q(owner=other))
    #         ).order_by('-date').first()
    #         context["message"].append([other, message])
    #     return context



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        others = Member.objects.all().exclude(pk=self.request.user.pk)
        query = self.request.GET.get('query')
        if query:
            others=others.filter(username__incontains=query)   
        user = self.request.user
        message = others.annotate(
            # owner__date__max=Max("owner__date", filter=Q(message_owner___friend)==user),
            # friend__date__max=Max("friend__date", filter=Q(message_friend___ower)==user),
            Max("message_owner__date"),
            Max("message_friend__date"),
            tem_latest_time=Greatest("message_owner__date__max", "message_friend__date__max"),
            latest_time=Coalesce("tem_latest_time", "message_owner__date__max", "message_friend__date__max"),
            latest_talk=Case(
                When(message_owner__date__lte=F("message_friend__date"), then=F("message_friend__message")),
                When(message_friend__date__lt=F("message_owner__date"), then=F("message_owner__message"))
            ),
        ).order_by("-latest_time").values("username", "id", "latest_time", "latest_talk", "img")
        context['message'] = message
        
        return context
    
           
        

    


class TalkRoomView(LoginRequiredMixin, generic.FormView):
    template_name = "myapp/talk_room.html"
    form_class = MessageForm
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        other = Member.objects.get(pk=self.kwargs['pk'])
        context['other'] = other
        context['message'] = Message.objects.select_related('friend', 'owner').all().filter(
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
        context['message'] = Message.objects.select_related('friend', 'owner').all().filter(
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
        
        return render(request, self.template_name, 
        {'form':self.form_class,
        'other':context['other'],
        'message':context['message'],
        'user': context['user'],}) 

    def get_success_url(self):
        return reverse_lazy('talk_room', kwargs={'pk': self.kwargs['pk']})
        


    


class SettingView(LoginRequiredMixin, generic.TemplateView):
    template_name = "myapp/setting.html"


class UserView(LoginRequiredMixin, generic.FormView):
    template_name = "myapp/user.html"
    form_class = UserForm

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(to='userdone')
        return render(request, self.template_name, {"form": form})




class UserdoneView(generic.TemplateView):
    template_name = 'myapp/userdone.html'



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




class MaildoneView(generic.TemplateView):
    template_name = 'myapp/maildone.html'



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
        



class ImgdoneView(generic.TemplateView):
    template_name = 'myapp/imgdone.html'
     

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



class PassworddoneView(generic.TemplateView):
    template_name = 'myapp/passworddone.html'


class LogoutView(LogoutView):
    success_url = reverse_lazy('myapp/index.html')






    
        