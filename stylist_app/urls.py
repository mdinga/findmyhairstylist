from django.urls import path
from django.contrib.auth import views as auth_views #so that we don't confuse with our own views (allows us to use LoginView and LogoutView)
from . import views

app_name = 'stylist_app'

urlpatterns = [
    path('stylist_home/', views.StylistHome.as_view(), name = 'stylist_home'),
    path('stylist_detail/<int:pk>/', views.viewStylist, name = 'stylist_detail'),
    path('stylists', views.listStylists, name = 'stylists_view'),
    path('stylist_update/<int:pk>/', views.updateStylist, name = 'stylist_update'),
    path('stylist_contact/<int:pk>/', views.updateStylistContact, name = 'stylist_contact_update'),
    path('service_create/<int:pk>/', views.createService, name = 'service_create'),
    path('service_update/<int:pk>/', views.updateService, name = 'service_update'),
    path('service_delete/<int:pk>/', views.deleteService, name = 'service_delete'),
    path('salon_create/<int:pk>/', views.createSalon, name = 'salon_create'),
    path('portfolio_item_create/<int:pk>/', views.createPortfolio, name = 'portfolio_item_create'),
    path('portfolio_view/<int:pk>/', views.viewPortfolio, name = 'portfolio_view'),
    path('portfolio_update/<int:pk>/', views.updatePortfolio, name = 'portfolio_update'),
    path('portfolio_delete/<int:pk>/', views.deletePortfolio, name = 'portfolio_delete'),
    path('search_stylist/', views.searchStylist, name='search'),
    path('searched_stylist/<region_pk>/<hairstyle_pk>/', views.searchedStylists, name='searched_stylists')

]
