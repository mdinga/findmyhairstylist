from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail

from accounts.models import User, Stylist, Client, City, Region
from accounts.forms import StylistSignupForm, ClientSignupForm
from django.contrib.auth.decorators import login_required
from django.views.generic import (CreateView, DeleteView)

import os
from django.conf import settings



def index(request):
    return render(request, 'index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def user_login(request):
    if request.method == 'POST':

        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user:
            if user.is_active and user.is_stylist:
                login(request, user)
                messages.success(request, 'Log In Successful')
                return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk':user.stylist.pk}))
            elif user.is_active and user.is_client:
                login(request, user)
                messages.success(request, 'Log In Successful')
                return HttpResponseRedirect(reverse('client_app:client_detail', kwargs={'pk':user.client.pk}))
            elif user.is_active and user.is_staff:
                login(request, user)
                return HttpResponseRedirect(reverse('admin_page'))
            else:
                messages.error(request,'Account in not active')
                return redirect('index')
        else:
            messages.error(request,'Your email or password is incorrect, please try again')
            return HttpResponseRedirect(reverse('accounts:login'))
    else:
        return render(request, 'accounts/login.html', {})

class StylistSignUp(CreateView):
    model = User
    form_class = StylistSignupForm
    success_url = reverse_lazy('accounts:stylist_success')
    template_name = 'accounts/stylist_signup.html'


class ClientSignUp(CreateView):
    model = User
    form_class = ClientSignupForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/client_signup.html'

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('home')


def stylist_signup_success(request):
    subject = "New Hairstylist Has Signed up"
    message = "Congratulations, A new haistylist has signed up."
    email = "DONOTREPLAY@findmyhairstylist.co.za"
    send_mail(subject, message, email, ['mbasa@findmyhairstylist.co.za'], fail_silently=False,)
    return render(request, 'accounts/stylist_success.html', {})
