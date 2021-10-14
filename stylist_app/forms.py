from django import forms
from accounts.models import Stylist, ServiceOffering, Salon, Portfolio, City, Region
from stylist_app.models import HairstyleCategory, Hairstyle
from django.core.exceptions import ValidationError



class StylistForm(forms.ModelForm):

    class Meta:
        model = Stylist
        fields = ['profile_pic', 'bio']
        field_order = ['profile_pic', 'bio']

        labels = {
            'bio': 'Bio (Limit: 256 Characters)',
        }
        widgets = {
            'profile_pic':forms.FileInput(attrs={'class':'form-control'}),
            'bio': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'e.g: Tell your clients why you love being a hairstylist.'}),
        }

class StylistContactForm(forms.ModelForm):

    class Meta:
        model = Stylist
        fields = ['phone_number', 'house_calls', 'salon', 'city', 'region', 'facebook', 'instagram']
        field_order = ['phone_number', 'house_calls', 'city', 'region', 'salon', 'facebook', 'instagram']


        labels = {
            'phone_number': 'Phone Number:',
            'house_calls': 'Do you do House Calls?:',
            'city': 'City:',
            'region': 'Neighbourhood:',
            'salon': 'Salon Name (if applicable):',
            'facebook': 'Facebook Page Link:',
            'instagram': 'Instagram Page Link:'
        }

        widgets = {

            'phone_number': forms.TextInput(attrs={'class':'form-control mb-4'},),
            'house_calls': forms.NullBooleanSelect(attrs={'class':'form-control mb-4'}),
            'city': forms.Select(attrs={'class':'form-control mb-4'}),
            'region': forms.Select(attrs={'class':'form-control mb-4'}),
            'salon':forms.Select(attrs={'class':'form-control mb-4'} ),
            'facebook': forms.URLInput(attrs={'class':'form-control mb-4', 'placeholder': 'Enter your full Facbook Page Link'}),
            'instagram': forms.URLInput(attrs={'class':'form-control mb-4', 'placeholder': 'Enter your full Instagram Page Link'})
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['region'].queryset = Region.objects.none()
            self.fields['salon'].queryset = Salon.objects.order_by('name')

            if 'city' in self.data:
                try:
                    city_id = int(self.data.get('city'))
                    self.fields['region'].queryset = Region.objects.filter(city_id=city_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['region'].queryset = self.instance.city.region_set.order_by('name')


class ServiceForm(forms.ModelForm):

    class Meta:
        model = ServiceOffering
        fields = ['category', 'hairstyle', 'description', 'price', 'top_style']

        labels = {
            'category': 'Select Category',
            'hairstyle': 'Select Hairstyle',
            'description': 'More Info (Limit: 120 Characters)',
            'price': 'Add Price',
            'top_style': 'I Specialize in this Style (Can only have 3 Specialize Styles)'
        }

        widgets = {
            'category' : forms.Select(attrs={'class': 'form-control mb-4', 'id': 'category_input'}),
            'hairstyle': forms.Select(attrs={'class': 'form-control mb-4', 'id': 'hairstyle_input'}),
            'description': forms.Textarea(attrs={'placeholder': 'Optional: Provide additional details on this hairstyle', 'class': 'form-control mb-4', 'id':'info_input'}),
            'price': forms.TextInput(attrs={'placeholder': 'Optional (Leave blank for POA)', 'class': 'form-control mb-4', 'id':'price_input'}),
            'top_style': forms.NullBooleanSelect(attrs={'class': 'form-control mb-4', 'id': 'specialize_input'})
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['hairstyle'].queryset = Hairstyle.objects.order_by('name')

            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['hairstyle'].queryset = Hairstyle.objects.filter(category_id=category_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['hairstyle'].queryset = self.instance.category.hairstyle_set.order_by('name')

        # def clean_top_style(self):
        #     cleaned_stylist = all_clean_data['stylist']
        #     cleaned_top_style = all_clean_data['top_style']
        #     top_styles = ServiceOffering.objects.filter(stylist=cleaned_stylist, top_style=cleaned_top_style)
        #     if top_styles.count() > 3:
        #         raise forms.ValidationError("Sorry, you can't have more than 3 Specialize Styles")


class Productform(forms.ModelForm):
    pass

class SalonForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = "__all__"

        labels = {
            'name': 'Salon Name',
            'phone_number': 'Salon Phone Number',
            'address': 'Street Number and Name'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'city': forms.Select(attrs={'class':'form-control mb-3'}),
            'region': forms.Select(attrs={'class':'form-control mb-3'}),
            'address': forms.Textarea(attrs={'class':'form-control mb-3'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control mb-3'})
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['region'].queryset = Region.objects.none()

            if 'city' in self.data:
                try:
                    city_id = int(self.data.get('city'))
                    self.fields['region'].queryset = Region.objects.filter(city_id=city_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['region'].queryset = self.instance.city.region_set.order_by('name')




class PortfolioForm(forms.ModelForm):

    class Meta:
        model = Portfolio
        fields = ['image', 'hairstyle', 'description']
        field_order = ['image', 'hairstyle', 'description']

        labels = {
            'hairstyle': 'Hairstyle Label',
            'product': 'Choose Product (if any)',
            'description': 'Description (optional):'
            }

        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control mb-3'}),
            'hairstyle': forms.Select(attrs={'class': 'form-control mb-3'}),
            'product': forms.Select(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3','placeholder': 'Tell your customers about this image. e.g. price, discounts etc'})}
