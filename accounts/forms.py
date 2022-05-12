# from allauth.account.forms import SignupForm
# from django import forms
# from .models import Member
# from allauth.account.adapter import DefaultAccountAdapter


# class CustomSignupForm(SignupForm):
#     img = forms.ImageField()
#     class Meta:
#         model = Member
#     def signup(self, request, user):
#         user.img = self.cleaned_data['img']
#         user.save()
#         return user
