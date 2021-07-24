from django.urls import path
from django.contrib.auth import views as auth_views #so that we don't confuse with our own views (allows us to use LoginView and LogoutView)
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('stylist_signup/', views.StylistSignUp.as_view(), name = 'stylist_signup'),
    path('client_signup/', views.ClientSignUp.as_view(), name = 'client_signup'),
    path('user_delete//<int:pk>/', views.UserDeleteView.as_view(), name = 'user_delete'),


]
