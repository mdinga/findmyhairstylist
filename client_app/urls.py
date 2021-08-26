from django.urls import path
from django.contrib.auth import views as auth_views #so that we don't confuse with our own views (allows us to use LoginView and LogoutView)
from . import views

app_name = 'client_app'

urlpatterns = [
    path('client_subscribe/', views.subscription, name='subscribe'),

]
