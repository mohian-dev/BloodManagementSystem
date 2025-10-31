from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from accounts.models import User, DonorProfile



class CustomUserAdmin(UserAdmin):

    list_display = ['username', 'email', 'is_donor', 'is_admin', 'is_staff']

    list_filter = ['is_donor', 'is_admin', 'is_staff']

    

    fieldsets = UserAdmin.fieldsets + (

        ('Role Information', {'fields': ('is_donor', 'is_admin')}),

    )



@admin.register(DonorProfile)

class DonorProfileAdmin(admin.ModelAdmin):

    list_display = ['full_name', 'blood_group', 'age', 'location', 'is_available', 'created_at']

    list_filter = ['blood_group', 'is_available']

    search_fields = ['full_name', 'phone', 'location']



admin.site.register(User, CustomUserAdmin)