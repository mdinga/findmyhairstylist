from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class HairstyleCategory(models.Model):
    name = models.CharField(max_length=128, blank=True)
    image = models.ImageField(upload_to='hairstyle_catergories/', blank=True)

    def __str__(self):
        return self.name

    def get_hairstyles(self):
        return Hairstyle.objects.filter(hairstyle_catergories=self.name)

class ProductCategory(models.Model):
    name = models.CharField(max_length=128, blank=True)
    image = models.ImageField(upload_to='product_catergories/', blank=True)

    def __str__(self):
        return self.name

class Hairstyle(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(HairstyleCategory, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(max_length=60, blank=True)
    hairstyle_image = models.ImageField(upload_to='hairstyle_eg/', blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(max_length=254, blank=True)
    product_image = models.ImageField(upload_to='product_eg/', blank=True)

    def __str__(self):
        return self.name




# Create your models here.
