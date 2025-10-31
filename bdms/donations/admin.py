from django.contrib import admin

from donations.models import DonationRequest, BloodInventory



@admin.register(DonationRequest)

class DonationRequestAdmin(admin.ModelAdmin):

    list_display = ['donor', 'request_date', 'preferred_date', 'status', 'approved_by']

    list_filter = ['status', 'request_date']

    search_fields = ['donor__full_name', 'donor__blood_group']



@admin.register(BloodInventory)

class BloodInventoryAdmin(admin.ModelAdmin):

    list_display = ['blood_group', 'units_available', 'last_updated']

    list_filter = ['blood_group']