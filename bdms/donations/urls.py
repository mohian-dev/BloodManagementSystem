from django.urls import path

from donations import views



urlpatterns = [

    # API endpoints

    path('request/', views.DonationRequestCreateView.as_view(), name='donation_request_api'),

    path('requests/', views.DonationRequestListView.as_view(), name='donation_requests_api'),

    path('request/<int:pk>/approve/', views.DonationRequestApprovalView.as_view(), name='approve_request_api'),

    path('inventory/', views.BloodInventoryListView.as_view(), name='inventory_api'),

    

    # Template views

    path('dashboard/', views.donor_dashboard, name='donor_dashboard'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('donation-request/', views.create_donation_request, name='create_donation_request'),

    path('donors/', views.donor_list_view, name='donor_list'),

    path('request/<int:pk>/approve/', views.approve_request, name='approve_request'),

]