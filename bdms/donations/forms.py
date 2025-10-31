from django import forms

from donations.models import DonationRequest



class DonationRequestForm(forms.ModelForm):

    class Meta:

        model = DonationRequest

        fields = ['preferred_date', 'units']

        widgets = {

            'preferred_date': forms.DateInput(attrs={

                'class': 'form-control',

                'type': 'date'

            }),

            'units': forms.NumberInput(attrs={

                'class': 'form-control',

                'min': 1,

                'max': 2,

                'value': 1

            }),

        }