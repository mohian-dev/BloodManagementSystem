from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

bloodGroup_choices = [('A+', 'A+'),('A-','A-'),('B+','B-'),('O+','O-')]

is_donor = models.BooleanField(default=True)
is_admin = models.BooleanField(default=True)

def save(self, *arg, **kwargs):
    if not self.pk:
        if self.is_staff or self.is_superuser:
            self.is_admin = True
            self.is_donor = False
        else:
            self.donor=True
            self.is_admin=False
    super.save(*args,**kwargs)


class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name=donor_profile)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=11)
    blood_group = models.CharField(choices=bloodGroup_choices)
    location = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    created_at= models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    class Meta:
        order = ['-created_at']
    def clean(self):
        if self.age<18 or self.age>65:
            raise ValidationError:("Age must be between 18 and 65 to be eligible for blood donation.")

    def __str__(self):
        return f"{self.full_name} - {self.blood_group} - {self.phone}" 

