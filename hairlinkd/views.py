from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from accounts import models
from stylist_app.models import HairstyleCategory, Hairstyle

def home_page(request):
    stylists = models.Stylist.objects.all()[:3]
    services = models.ServiceOffering.objects.filter(stylist__in=stylists)
    regions = models.Region.objects.filter(stylist__in=stylists).distinct().order_by('city')

    context = {'stylists':stylists, 'services':services, 'regions':regions}
    return render(request, 'index.html', context)


class TestPage(TemplateView):
     template_name = 'test.html'

class ThanksPage(TemplateView):
     template_name = 'thanks.html'

def contact(request):
    return render(request, 'contact.html')

# ajax

def load_regions(request):
    city_id = request.GET.get('city')
    regions = Region.objects.filter(city_id=city_id).all()
    context = {'regions':regions}
    return render(request, 'region_dropdown_options.html', context)

def load_hairstyles(request):
    category_id = request.GET.get('category')
    hairstyles = Hairstyle.objects.filter(category_id=category_id).all()
    context = {'hairstyles': hairstyles}
    return render(request, 'hairstyle_dropdown_options.html', context)
