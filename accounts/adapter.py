# from allauth.accounts.adapter import DefaultAccountAdapter

# class AccountAdapter(DefaultAccountAdapter):

#     def save_user(self, request, user, form, commit=True ):

#         user = super(AccountAdapter, self ).save_user(request, user, form, commit=True)
#         user.img = form.cleaned_data.get('img')
#         user.save
