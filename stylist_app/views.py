from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import (TemplateView)
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts import models
from stylist_app.models import Hairstyle, Product, HairstyleCategory
from .forms import StylistForm, ServiceForm, SalonForm, PortfolioForm, StylistContactForm
from accounts.forms import UserForm


class StylistHome(TemplateView):
     template_name = 'stylist_home.html'

## -------------------------------Stylist Functions________________________________________________

def is_valid_queryparam(param):
    return param != '' and param is not None

def listStylists(request):
    # stylists = models.Stylist.objects.all().order_by('-user__date_joined')
    stylists = models.Stylist.objects.all().order_by('user__name')
    hairstyles = models.Hairstyle.objects.filter(stylist__in =stylists).distinct().order_by('category')
    services = models.ServiceOffering.objects.filter(stylist__in=stylists)
    regions = models.Region.objects.filter(stylist__in=stylists).distinct().order_by('city')

    # city = models.City.objects.filter(region__in=regions).distinct()


    name_query = request.GET.get('stylist_name')
    region_query = request.GET.get('region_name')
    hairstyle_query = request.GET.get('hairstyle_name')
    house_call_query = request.GET.get('house_call')
    # signiture_query = request.GET.get('signiture_hairstyle_name')
    # rating_query = request.GET.get('rating_name')
    # city_query = request.GET.get('city_name')



    if is_valid_queryparam(name_query):
        stylists = stylists.filter(user__name__icontains=name_query)

    if is_valid_queryparam(region_query):
        stylists = stylists.filter(Q(region__name = region_query))

    if is_valid_queryparam(hairstyle_query):
         stylists = stylists.filter(hairstyles__name = hairstyle_query)

    if house_call_query == 'on':
        stylists = stylists.filter(house_calls=True)

    p = Paginator(stylists, 6)

    page_num = request.GET.get('page', 1)

    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    context = {'stylists':page, 'hairstyles':hairstyles, 'services':services, 'regions':regions}
    return render(request, 'stylist_app/view_stylists.html', context)

def searchedStylists(request, region_pk, hairstyle_pk):

    if region_pk != 'None':
        stylists = models.Stylist.objects.filter(region__pk = int(region_pk))
    else:
        hairstyle = models.Hairstyle.objects.get(pk = int(hairstyle_pk))
        stylists = hairstyle.stylist_set.all()


    services = models.ServiceOffering.objects.filter(stylist__in=stylists)

    context = {'stylists':stylists, 'services':services}
    return render(request, 'stylist_app/searched_stylists.html', context)

@login_required
def viewStylist(request, pk):
    user = request.user
    stylist = models.Stylist.objects.get(pk=pk)
    reviews = models.Review.objects.filter(stylist=stylist)
    services = stylist.stylist_hairstyles.all()
    portfolio = stylist.portfolio_set.all()
    category = []

    for service in services:
        category.append(service.category)
    categories = set(category)

    profile_items = {'profile_pic': 0, 'bio':0,
                    'region':0, 'hairstyle':0,
                    'portfolio':0, 'phone':0}
    completeness = 0
    if stylist.profile_pic != "profile_pics/default_stylist.png":
        profile_items['profile_pic'] = 1
    if stylist.bio:
        profile_items['bio'] = 1
    if stylist.region:
        profile_items['region'] = 1
    if stylist.stylist_hairstyles.first():
        profile_items['hairstyle'] = 1
    if stylist.portfolio_set.first():
        profile_items['portfolio'] = 1
    if stylist.phone_number:
        profile_items['phone'] = 1

    for k, v in profile_items.items():
        completeness += v
        profile_completeness = (completeness/6)*100

    context = {'user': user, 'services': services, 'stylist': stylist,
                'portfolio': portfolio, 'categories': categories,
                'profile_completeness':profile_completeness,
                'profile_items':profile_items, 'reviews': reviews}
    return render(request, 'stylist_app/stylist_detail.html', context)



def updateStylist(request, pk):
    stylist = models.Stylist.objects.get(pk=pk)
    form = StylistForm(instance=stylist)
    user_form = UserForm(instance=stylist.user)

    if request.method == 'POST':
        form = StylistForm(request.POST, request.FILES, instance=stylist)
        user_form = UserForm(request.POST, instance=stylist.user)
        if form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, 'Your profile has been updated')
            return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))
        else:
            return HttpResponse("Oops looks like something went wrong. Please try again")

    context = {'form':form, 'user_form': user_form}
    return render(request, 'stylist_app/stylist_form.html', context)

def updateStylistContact(request, pk):
    stylist = models.Stylist.objects.get(pk=pk)
    contact_form = StylistContactForm(instance=stylist)

    if request.method == 'POST':
        contact_form = StylistContactForm(request.POST, instance=stylist)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Your contact details have been updated')
            return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))

    context = {'contact_form':contact_form}
    return render(request, 'stylist_app/stylist_contact_form.html', context)



##---------------------------------------------Services ---------------------------------------------------------------------------

def limit_top_styles(styles, limit):
    if styles.filter(top_style=True).all().count() < limit:
        return True
    else:
        return False




def createService(request, pk):
    stylist = models.Stylist.objects.get(pk=pk)
    current_services = stylist.stylist_hairstyles.all()
    form = ServiceForm

    if current_services.count() > 9:
        messages.error(request, "Sorry, you can't have more than 10 hairstyles")
        return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.stylist = stylist
            if instance.top_style == True:
                if limit_top_styles(current_services, 3):
                    try:
                        instance.save()
                        messages.success(request, 'Hairstyle has been added')
                        return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))
                    except IntegrityError:
                        return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))
                        messages.error(request, 'Sorry, you already have this hairstyle')
                else:
                    messages.error(request, "Sorry, you can't have more than 3 signiture hairstyles")
                    return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))
            else:
                try:
                    instance.save()
                    messages.success(request, 'Hairstyle has been added')
                    return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))
                except IntegrityError:
                    return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))
                    messages.error(request, 'Sorry, you already have this hairstyle')

    context = {'form':form}
    return render(request, 'stylist_app/hair_form.html', context)

def updateService(request, pk):
    service = models.ServiceOffering.objects.get(pk=pk)
    stylist = service.stylist
    current_services = stylist.stylist_hairstyles.all()

    form = ServiceForm(instance=service)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            if limit_top_styles(current_services, 3):
                try:
                    form.save()
                    messages.success(request, 'Hairstyle has been updated')
                    return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))
                except IntegrityError:
                    messages.error(request, 'Sorry, you already have this hairstyle')
                    return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))
            else:
                messages.error(request, "Sorry, you can't have more than 3 signiture hairstyles")
                return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))

    context = {'form':form}
    return render(request, 'stylist_app/hair_form.html', context)


def deleteService(request, pk):
    service = models.ServiceOffering.objects.get(pk=pk)
    stylist = service.stylist

    if request.method == 'POST':
        service.delete()
        messages.error(request, 'Hairstyle has been removed')
        return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))

    context = {'service': service}
    return render(request, 'stylist_app/delete_service.html', context)

##---------------------------------------------Salon ---------------------------------------------------------------------------


def createSalon(request, pk):
    stylist = request.user.stylist
    form = SalonForm
    if request.method == 'POST':
        form = SalonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your salon has been added to the list')
            return HttpResponseRedirect(reverse('stylist_app:stylist_contact_update', kwargs={'pk': stylist.pk}))

    context = {'form': form, 'pk':pk}
    return render(request, 'stylist_app/create_salon.html', context)

##---------------------------------------------Portfolio ---------------------------------------------------------------------------

def createPortfolio(request, pk):
    stylist = models.Stylist.objects.get(pk=pk)
    form = PortfolioForm

    if stylist.portfolio_set.all().count() > 5:
        messages.error(request, "You can't have more than 6 gallery items")
        return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))

    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.stylist = stylist
            instance.save()
            messages.success(request, 'An item has been added to your gallery')
            return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))




    context = {'form': form, 'stylist':stylist}
    return render(request, 'stylist_app/portfolio_form.html', context)

def updatePortfolio(request, pk):
    item = models.Portfolio.objects.get(pk=pk)
    stylist = item.stylist
    form = PortfolioForm(instance = item)

    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'An item has been updated in your gallery')
            return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))
        else:
            return HttpResponse("Oops looks like something went wrong. Please try again")

    context = {'form':form, 'stylist':stylist}
    return render(request, 'stylist_app/portfolio_form.html', context)


def deletePortfolio(request, pk):
    item = models.Portfolio.objects.get(pk=pk)
    stylist = item.stylist

    if request.method == 'POST':
        item.delete()
        messages.error(request, 'An item has been removed from your gallery')
        return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))

    context = {'item': item, 'stylist':stylist}
    return render(request, 'stylist_app/delete_portfolio.html', context)


def viewPortfolio(request, pk):
    pass


# --------------------------------Search Stylist------------------------------------------

def searchStylist(request):
    stylists = models.Stylist.objects.all()
    cities = models.City.objects.all()
    categories = models.HairstyleCategory.objects.all()
    regions = []
    hairstyles = []

    for stylist in stylists:
        regions.append(stylist.region)
        for hairstyle in stylist.hairstyles.all():
            hairstyles.append(hairstyle)

    regions = set(regions)
    hairstyles = set(hairstyles)


    context = {'stylists': stylists, 'cities': cities,
                'regions': regions, 'categories':categories,
                'hairstyles': hairstyles}
    return render(request, 'stylist_app/search_stylist.html', context)
