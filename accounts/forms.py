from django import forms
from accounts.models import Stylist, Client, User
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name']

        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),

        }

class StylistSignupForm(UserCreationForm):

    #password = forms.CharField(widget = forms.PasswordInput())  #editing existing attributes

    class Meta():
        model = User
        fields = ('email', 'name')

        # widgets = {
        #     'email': forms.TextInput(attrs={'class':'group'}),
        #     'name': forms.TextInput(attrs={'class':'group'}),
        #     'password': forms.PasswordInput(attrs={'class':'group'}),
        # }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['name'].label = 'Name'



    @transaction.atomic
    def save(self):
        user = super().save(commit = False)
    #add additional attributes for the user e.g user.name = self.cleaned_data.get('name')
        user.is_stylist = True
        user.email = user.email.lower()
        user.save()
        stylist = Stylist.objects.create(user=user)
    #add other attributes for the sylist that you want
        stylist.save()
        return user




class ClientSignupForm(UserCreationForm):

    #password = forms.CharField(widget = forms.PasswordInput())  #editing existing attributes

    class Meta():
        model = User
        fields = ('email', 'name')

    @transaction.atomic
    def save(self):
        user = super().save(commit = False)
        #add additional attributes for the user e.g user.name = self.cleaned_data.get('name')
        user.is_client = True
        user.save()
        client = Client.objects.create(user=user)
        #add other attributes for the sylist that you want
        client.save()
        return user
