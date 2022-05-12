from django.contrib import admin
from .models import Message, Member
from django.contrib.auth.admin import UserAdmin

#Register your models here.

class CustomUserAdmin(UserAdmin):
    model = Member
    fieldsets = UserAdmin.fieldsets+((None, {'fields': ('img',)}),)
    list_display = ['username', 'email', 'img']


admin.site.register(Message,admin.ModelAdmin)
admin.site.register(Member)

