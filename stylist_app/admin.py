from django.contrib import admin
from .models import Hairstyle, Product, HairstyleCategory, ProductCategory


admin.site.register(Hairstyle)
admin.site.register(Product)
admin.site.register(HairstyleCategory)
admin.site.register(ProductCategory)


# Register your models here.
