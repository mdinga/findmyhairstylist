from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Region, City, Stylist, ServiceOffering
from stylist_app.models import HairstyleCategory, Hairstyle
from django.core.mail import send_mail
from django.contrib import messages
from django.core.files import File

def home_page(request):
    stylists = Stylist.objects.all()[:3]
    services = ServiceOffering.objects.filter(stylist__in=stylists)
    regions = Region.objects.filter(stylist__in=stylists).distinct().order_by('city')

    messages.success(request, 'Hairstylists from Fourways and Sandton area are invited to Sign Up for FREE')
    context = {'stylists':stylists, 'services':services, 'regions':regions}
    return render(request, 'index.html', context)


class TestPage(TemplateView):
     template_name = 'test.html'

class ThanksPage(TemplateView):
     template_name = 'thanks.html'

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')
        address = request.POST.get('address')

        if not address:
            send_mail(
                subject,
                message,
                email,
                ['mbasa@findmyhairstylist.co.za'],
                fail_silently=False,)

        context = {'name': name, 'subject': subject, 'email':email, 'message': message }
        return render(request, 'contact.html', context)
    else:
        return render(request, 'contact.html', {})

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


def view_admin(request):
    cities = City.objects.order_by("name")
    regions = Region.objects.order_by("name")

    context = {'cities': cities, 'regions':regions}
    return render (request, 'admin_page.html', context)

def update_city(request, pk):
    pass
