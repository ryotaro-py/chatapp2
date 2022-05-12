# from django.shortcuts import render
# from allauth.account.views import SignupView as AllAuthSignupView

# class SignupView(AllAuthSignupView):
#     template_name = 'accounts/signup.html'
#     model = Member
#     form_class = CustomSignupForm

#     def Post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             return 
#         return render(request, self.template_name, {'form',form})


