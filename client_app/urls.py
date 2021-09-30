from django.urls import path
from django.contrib.auth import views as auth_views #so that we don't confuse with our own views (allows us to use LoginView and LogoutView)
from . import views

app_name = 'client_app'

urlpatterns = [
    path('client_subscribe/', views.subscription, name='subscribe'),
    path('client_detail/<int:pk>/', views.viewClient, name='client_detail'),
    path('add_favourite/<int:pk>/', views.addFavourite, name='add_favourite'),
    path('remove_favourite/<int:pk>/', views.removeFavourite, name='remove_favourite'),
    path('add_review/<int:pk>/', views.addReview, name='add_review'),
    path('view_review/<int:pk>/', views.viewReview, name='view_review'),
    path('update_review/<int:pk>/', views.updateReview, name='update_review'),
    path('delete_review/<int:pk>/', views.deleteReview, name='delete_review'),
    
]
