"""hairlinkd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home_page, name="home"),
    path('admin/', admin.site.urls),
    path('test/', views.TestPage.as_view(), name='test'),
    path('thanks/', views.ThanksPage.as_view(), name='thanks'),
    path('contact/', views.contact, name='contact'),
    path('accounts/', include('accounts.urls')),
    path('stylist_app/', include('stylist_app.urls', namespace = 'stylists')),
    path('stylist_app/', include('django.contrib.auth.urls')),
    path('client_app/', include('client_app.urls', namespace = 'clients')),
    path('ajax/load-regions/', views.load_regions, name='ajax_load_regions'),
    path('ajax/load-hairstyles', views.load_hairstyles, name='ajax_load_hairstyles'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
