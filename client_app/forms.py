from django import forms
from django.forms.widgets import NumberInput
from accounts.models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['appointment', 'value', 'hygiene', 'expectation',
                    'craft', 'professional', 'comment', 'recommendation']
        field_order = ['appointment', 'value', 'hygiene', 'expectation',
                    'craft', 'professional', 'comment', 'recommendation']

        labels = {
            'appointment': 'Date of Appointment',
            'value': 'Value for My Money',
            'hygiene': 'Hygiene (e.g. Covid precautions, cleanliness)',
            'expectation': 'Expectations Met (I got what I was looking for)',
            'craft': 'Craft ( e.g. Skill, Creativity, Care, Condifence)',
            'professional':'Professionalism (e.g. Time management, Communication, Focus)',
            'recommendation': 'Would you recommend this hairstylist?'
        }

        SCORES =[
            ('1', '1'),('2', '2'),
            ('3', '3'),('4', '4'),
            ('5', '5'),
        ]


        widgets = {
            'appointment' : forms.DateInput(attrs={'type':'date', 'class':'form-control mb-4'}),
            'value' : forms.Select(attrs={'class': 'form-control mb-4'}),
            'hygiene' : forms.Select(attrs={'class': 'form-control mb-4'}),
            'expectation' : forms.Select(attrs={'class': 'form-control mb-4'}),
            'craft' : forms.Select(attrs={'class': 'form-control mb-4'}),
            'professional' : forms.Select(attrs={'class': 'form-control mb-4'}),
            'comment' : forms.Textarea(attrs={'placeholder': 'Tell us more. e.g. Why did you rate as you did? Any room for improvement?', 'class': 'form-control mb-4'}),
            'recommendation' : forms.NullBooleanSelect(attrs={'class': 'form-control mb-4'}),
        }
