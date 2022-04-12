from django import forms
from .models import Member, Message
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class InquiryForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ('username', 'email', 'img',)  
        labels = {'username':'Username',  'email':'Emailaddress',  'img':'img'}

class LoginForm(AuthenticationForm):
    class Meta:
        model = Member
        fields = ('username',)
        labels = {'username':'Username'}

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('message',)
        
class UserForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('username',)

class MailForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('email',)

class ImgForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('img',)