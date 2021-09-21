from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from mailchimp_marketing import Client
from accounts import models
from mailchimp_marketing.api_client import ApiClientError
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID


@login_required
def viewClient(request, pk):
    client = models.Client.objects.get(pk = pk)

    context = {'client':client}
    return render(request, 'client_app/client_details.html', context)

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
