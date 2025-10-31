from django.contrib import admin

from django.urls import path, include



urlpatterns = [

    path('admin/', admin.site.urls),

    path('api/auth/', include('accounts.urls')),

    path('api/donations/', include('donations.urls')),

    path('', include('accounts.urls')),

    path('', include('donations.urls')),

]