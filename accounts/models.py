from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator, MaxLengthValidator
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill



from stylist_app.models import Hairstyle, Product, HairstyleCategory


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_stylist = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def get_email(self):
        return self.email

class City(models.Model):
    name = models.CharField(max_length = 100, blank=True)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length = 100, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Salon(models.Model):

    name = models.CharField(max_length=128)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.TextField(max_length=128, blank=True)
    phone_number = models.CharField(max_length = 20, null=True, blank=True)

    def __str__(self):
        return self.name

class Stylist(models.Model):

    phone_regex = RegexValidator(regex=r'\d{9,15}', message="Phone number has a minimum of 9 characters and a maximum of 15")

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_pic = ProcessedImageField(upload_to = 'profile_pics/',
                                        processors=[ResizeToFill(280,280)],
                                        format='PNG',
                                        options={'quality':100},
                                        default='profile_pics/default_stylist.png')
    phone_number = models.CharField(max_length=17, validators=[phone_regex], blank=True)
    bio = models.TextField(max_length=256)
    house_calls =models.BooleanField(default=False)
    facebook = models.URLField(blank = True)
    instagram = models.URLField(blank = True)
    rating = models.FloatField(default = 0.0)
    hairstyles = models.ManyToManyField(Hairstyle, through='ServiceOffering')
    product = models.ManyToManyField(Product, through='ProductOffering')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    salon = models.ForeignKey(Salon, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.user.name

    def get_absolute_url(self):
        return reverse('stylist_app:stylist_detail', kwargs={'pk': self.pk})
            #always return to the detail page of the primary key that was worked on



class ServiceOffering(models.Model):
    hairstyle = models.ForeignKey(Hairstyle,
                                    related_name='style_offers',
                                    on_delete=models.CASCADE)
    category = models.ForeignKey(HairstyleCategory,
                                    related_name='style_categories',
                                    on_delete=models.CASCADE, blank=True, null=True)
    stylist = models.ForeignKey(Stylist,
                                    related_name='stylist_hairstyles',
                                    on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=True)
    description = models.TextField(max_length=120, blank=True)
    price = models.FloatField(blank=True, null=True)
    top_style = models.BooleanField(default=False)


    class Meta:
        unique_together = ('hairstyle', 'stylist')



class ProductOffering(models.Model):
    product = models.ForeignKey(Product,
                                    related_name='product_offer',
                                    on_delete=models.CASCADE)

    stylist = models.ForeignKey(Stylist,
                                    related_name='stylist_product',
                                    on_delete=models.CASCADE)

    name = models.CharField(max_length=128)
    description = models.TextField(max_length=254, blank=True)
    price = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ('product', 'stylist')

class Portfolio(models.Model):
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE)
    hairstyle = models.ForeignKey(Hairstyle, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(max_length= 128, null=True, blank=True)
    likes = models.IntegerField(default = 0)
    image = models.ImageField(upload_to='portfolio_pics/')
    image_thumbnail = ImageSpecField(source='image',processors=[ResizeToFill(280, 280)], format='JPEG', options={'quality': 200} )


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    fav_hairstlye = models.CharField(max_length=254, null=True, blank=True)


# Create your models here.
