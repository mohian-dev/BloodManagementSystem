from django.urls import path

from accounts import views



urlpatterns = [

    # API endpoints

    path('register/', views.register_api, name='register_api'),

    path('login/', views.login_api, name='login_api'),

    path('logout/', views.logout_api, name='logout_api'),

    path('profile/', views.DonorProfileView.as_view(), name='profile_api'),

    path('donors/', views.DonorListView.as_view(), name='donor_list_api'),

    

    # Template views

    path('register/', views.register_view, name='register'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile_view, name='profile'),

]