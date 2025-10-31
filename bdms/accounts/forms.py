from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model

from accounts.models import DonorProfile, BLOOD_GROUPS



User = get_user_model()



class DonorRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    full_name = forms.CharField(max_length=200, required=True)

    age = forms.IntegerField(min_value=18, max_value=65, required=True)

    phone = forms.CharField(max_length=15, required=True)

    blood_group = forms.ChoiceField(choices=BLOOD_GROUPS, required=True)

    location = forms.CharField(max_length=200, required=True)

    

    class Meta:

        model = User

        fields = ['username', 'email', 'password1', 'password2']

    

    def save(self, commit=True):

        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        user.is_donor = True

        

        if commit:

            user.save()

            DonorProfile.objects.create(

                user=user,

                full_name=self.cleaned_data['full_name'],

                age=self.cleaned_data['age'],

                phone=self.cleaned_data['phone'],

                blood_group=self.cleaned_data['blood_group'],

                location=self.cleaned_data['location'],

            )

        return user



class DonorProfileForm(forms.ModelForm):

    class Meta:

        model = DonorProfile

        fields = ['full_name', 'age', 'phone', 'blood_group', 'location', 'is_available']

        widgets = {

            'full_name': forms.TextInput(attrs={'class': 'form-control'}),

            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 18, 'max': 65}),

            'phone': forms.TextInput(attrs={'class': 'form-control'}),

            'blood_group': forms.Select(attrs={'class': 'form-control'}),

            'location': forms.TextInput(attrs={'class': 'form-control'}),

            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }