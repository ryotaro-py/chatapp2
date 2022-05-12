from django.db import models
from django.contrib.auth.models import AbstractUser
# from accounts.models import Member


class Member(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100)
    img = models.ImageField(
        upload_to = 'files/',
        verbose_name = '添付画像',)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('date', )




class Message(models.Model):
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, related_name='message_owner')
    friend = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, related_name='message_friend')
    message = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class Meta:
        ordering = ('-date', )












