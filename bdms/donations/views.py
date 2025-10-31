from django.shortcuts import render,redirect, get_object_or_404

# Create your views here.
from rest_framework import generics, permissions, status

from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response


from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.db.models import Count, Sum

from django.utils import timezone

from donations.models import DonationRequest, BloodInventory

from donations.serializers import (

    DonationRequestSerializer, 

    DonationRequestApprovalSerializer,

    BloodInventorySerializer

)

from donations.forms import DonationRequestForm

from accounts.models import DonorProfile



class DonationRequestCreateView(generics.CreateAPIView):

    serializer_class = DonationRequestSerializer

    permission_classes = [permissions.IsAuthenticated]

    

    def perform_create(self, serializer):

        donor_profile = self.request.user.donor_profile

        serializer.save(donor=donor_profile)



class DonationRequestListView(generics.ListAPIView):

    serializer_class = DonationRequestSerializer

    permission_classes = [permissions.IsAuthenticated]

    

    def get_queryset(self):

        if self.request.user.is_admin:

            return DonationRequest.objects.all()

        return DonationRequest.objects.filter(donor__user=self.request.user)



class DonationRequestApprovalView(generics.UpdateAPIView):

    serializer_class = DonationRequestApprovalSerializer

    permission_classes = [permissions.IsAuthenticated]

    queryset = DonationRequest.objects.all()

    

    def perform_update(self, serializer):

        if not self.request.user.is_admin:

            return Response({'error': 'Admin access required'}, 

                          status=status.HTTP_403_FORBIDDEN)

        

        instance = serializer.save(

            approved_by=self.request.user,

            approved_date=timezone.now()

        )

        

        # Update inventory if approved

        if instance.status == 'completed':

            blood_group = instance.donor.blood_group

            inventory, created = BloodInventory.objects.get_or_create(

                blood_group=blood_group,

                defaults={'units_available': 0}

            )

            inventory.units_available += instance.units

            inventory.save()



class BloodInventoryListView(generics.ListAPIView):

    queryset = BloodInventory.objects.all()

    serializer_class = BloodInventorySerializer

    permission_classes = [permissions.IsAuthenticated]



# Template Views

@login_required

def donor_dashboard(request):

    if not request.user.is_donor:

        return redirect('admin_dashboard')

    

    profile = request.user.donor_profile

    donation_history = DonationRequest.objects.filter(donor=profile)

    inventory = BloodInventory.objects.all()

    

    context = {

        'profile': profile,

        'donation_history': donation_history,

        'inventory': inventory,

        'pending_count': donation_history.filter(status='pending').count(),

    }

    return render(request, 'donations/donor_dashboard.html', context)



@login_required

def admin_dashboard(request):

    if not request.user.is_admin:

        return redirect('donor_dashboard')

    

    total_donors = DonorProfile.objects.count()

    pending_requests = DonationRequest.objects.filter(status='pending').count()

    inventory = BloodInventory.objects.all()

    recent_requests = DonationRequest.objects.all()[:10]

    

    # Blood group statistics

    blood_stats = DonorProfile.objects.values('blood_group').annotate(

        count=Count('id')

    ).order_by('blood_group')

    

    context = {

        'total_donors': total_donors,

        'pending_requests': pending_requests,

        'inventory': inventory,

        'recent_requests': recent_requests,

        'blood_stats': blood_stats,

    }

    return render(request, 'donations/admin_dashboard.html', context)



@login_required

def create_donation_request(request):

    if not request.user.is_donor:

        return redirect('admin_dashboard')

    

    profile = request.user.donor_profile

    

    # Check for pending requests

    if DonationRequest.objects.filter(donor=profile, status='pending').exists():

        messages.error(request, 'You already have a pending donation request.')

        return redirect('donor_dashboard')

    

    if request.method == 'POST':

        form = DonationRequestForm(request.POST)

        if form.is_valid():

            donation_request = form.save(commit=False)

            donation_request.donor = profile

            donation_request.save()

            messages.success(request, 'Donation request submitted successfully!')

            return redirect('donor_dashboard')

    else:

        form = DonationRequestForm()

    

    return render(request, 'donations/request_form.html', {'form': form})



@login_required

def donor_list_view(request):

    donors = DonorProfile.objects.all()

    

    # Filters

    blood_group = request.GET.get('blood_group')

    is_available = request.GET.get('is_available')

    

    if blood_group:

        donors = donors.filter(blood_group=blood_group)

    if is_available:

        donors = donors.filter(is_available=is_available == 'true')

    

    context = {

        'donors': donors,

        'blood_groups': BLOOD_GROUPS,

        'selected_blood_group': blood_group,

        'selected_availability': is_available,

    }

    return render(request, 'donations/donor_list.html', context)



@login_required

def approve_request(request, pk):

    if not request.user.is_admin:

        messages.error(request, 'Admin access required')

        return redirect('donor_dashboard')

    

    donation_request = get_object_or_404(DonationRequest, pk=pk)

    

    if request.method == 'POST':

        action = request.POST.get('action')

        notes = request.POST.get('admin_notes', '')

        

        if action == 'approve':

            donation_request.status = 'approved'

        elif action == 'reject':

            donation_request.status = 'rejected'

        elif action == 'complete':

            donation_request.status = 'completed'

            # Update inventory

            blood_group = donation_request.donor.blood_group

            inventory, created = BloodInventory.objects.get_or_create(

                blood_group=blood_group,

                defaults={'units_available': 0}

            )

            inventory.units_available += donation_request.units

            inventory.save()

        

        donation_request.admin_notes = notes

        donation_request.approved_by = request.user

        donation_request.approved_date = timezone.now()

        donation_request.save()

        

        messages.success(request, f'Request {action}ed successfully!')

    

    return redirect('admin_dashboard') 