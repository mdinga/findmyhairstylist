from django.db import models
from accounts.models import Stylist, Client

class Favourite(models.Model):
    client = models.ForeignKey(Client, related_name='client_favourite'
                                ,on_delete=models.CASCADE)
    stylist = models.ForeignKey(Stylist, related_name='stylist_as_favourite'
                                ,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('client', 'stylist')





# Create your models here.
