from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from mailchimp_marketing import Client
from accounts.models import Stylist, Client, Review, ServiceOffering
from client_app.models import Favourite
from .forms import ReviewForm
from mailchimp_marketing.api_client import ApiClientError
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Avg


# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID


@login_required
def viewClient(request, pk):
    client = Client.objects.get(pk = pk)
    favourite_stylists = Favourite.objects.filter(client=client)
    reviews = Review.objects.filter(client=client)



    context = {'client':client, 'favourite_stylists':favourite_stylists, 'reviews':reviews}
    return render(request, 'client_app/client_details.html', context)


def addFavourite(request, pk):
    user = request.user
    client = user.client
    stylist = Stylist.objects.get(pk=pk)
    favourite = Favourite(client=client, stylist=stylist)
    try:
        favourite.save()
        messages.success(request, 'Added to your favourites')
        return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))
    except IntegrityError:
        messages.error(request, 'Oops, Looks like this hairstylist is already in your favourites')
        return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))


def removeFavourite(request, pk):
    client = request.user.client
    favourite = Favourite.objects.get(pk=pk)

    favourite.delete()
    return HttpResponseRedirect(reverse('client_app:client_detail', kwargs={'pk': client.pk}))


def updateTotalRating(pk):
    stylist = Stylist.objects.get(pk=pk)
    average_score = Review.objects.filter(stylist=stylist).aggregate(Avg('total_rating'))

    stylist.rating = average_score['total_rating__avg']

    if not stylist.rating:
        stylist.rating = 0.0
        
    stylist.save()


def addReview(request, pk):
    client = request.user.client
    stylist = Stylist.objects.get(pk=pk)
    rating = stylist.rating
    form = ReviewForm
    new_rating = 0

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.client = client
            instance.stylist = stylist
            instance.total_rating = (instance.value+instance.hygiene+instance.expectation+instance.craft+instance.professional)/5
            form.save()
            updateTotalRating(stylist.pk)

            messages.success(request, 'Your review has been added')
            return HttpResponseRedirect(reverse('client_app:view_review', kwargs={'pk': instance.pk}))

    context = {'form':form, 'stylist':stylist}
    return render(request, 'client_app/review.html', context)

def viewReview(request, pk):
    review = Review.objects.get(pk=pk)

    context = {'review': review}
    return render(request, 'client_app/view_review.html', context)

def updateReview(request, pk):
    review = Review.objects.get(pk=pk)
    client = review.client
    stylist = review.stylist

    form = ReviewForm(instance=review)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.total_rating = (instance.value+instance.hygiene+instance.expectation+instance.craft+instance.professional)/5
            form.save()
            updateTotalRating(stylist.pk)
            messages.success(request, 'Review updated')
            return HttpResponseRedirect(reverse('client_app:view_review', kwargs={'pk': review.pk}))

    context = {'form': form, 'stylist':stylist}
    return render(request, 'client_app/review.html', context)


def deleteReview(request, pk):
    review = Review.objects.get(pk=pk)
    client = review.client
    stylist = review.stylist

    if request.method == 'POST':
        review.delete()
        updateTotalRating(stylist.pk)
        messages.success(request, 'Your review has been deleted')
        return HttpResponseRedirect(reverse('stylist_app:stylist_detail', kwargs={'pk': stylist.pk}))

    context = {'review': review}
    return render(request, 'client_app/delete_review.html', context)

# Subscription Logic
def subscribe(email):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))


def subscription(request):
    if request.method == "POST":
        email = request.POST['email']
        name = request.POST['name']
        subject = 'New Subscriber'
        message = 'Congratulations, you have a new subscriber'

        if not name:
            subscribe(email)
            send_mail(
                subject,
                message,
                email,
                ['mbasa@findmyhairstylist.co.za'],
                fail_silently=False,
            )
            messages.success(request, "You have been subscribed. Thank You! ")
        else:
            messages.success(request, "Sent")
    return render(request, 'client_app/subscribe.html', {})
