# Generated by Django 3.2.2 on 2021-09-21 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20210921_1045'),
        ('client_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favourite',
            unique_together={('client', 'stylist')},
        ),
    ]
