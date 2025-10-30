from django.db import models
from django.contrib.auth.models import User
from accounts.models import DonorProfile

# Create your models here.
class BloodInventory(models.Model):
    blood_group = models.CharField(max_length=3)
    quantity_ml = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    class meta:
        verbose_name_Plural = "Blood Inventories"
        ordering = ['-blood_group']
    
    def __str__(self):
        return f"{self.blood_group}: {self.units_available} units"

class DonationRequest(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'),('approved', 'Approved'),('rejected', 'Rejected'),('completed','Completed'),]
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name='donation_requests')
    request_date = models.DateTimeField(auto_now_add=True)
    preferred_date = models.DateField()
    units = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requests')
    approved_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-request_date']
    
    def __str__(self):
        return f"{self.donor.full_name} - {self.status}"