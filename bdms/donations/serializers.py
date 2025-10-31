from rest_framework import serializers
from donations.models import DonationRequest, BloodInventory
#from accounts.serializers import DonorProfileSerializer

class BloodInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodInventory
        fields = ['id', 'blood_group', 'units_available', 'last_updated']
        read_only_fields = ['last_updated']

class DonationRequestSerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(source='donor.full_name', read_only=True)
    donor_blood_group = serializers.CharField(source='donor.blood_group', read_only=True)
    donor_phone = serializers.CharField(source='donor.phone', read_only=True)
    
    class Meta:
        model = DonationRequest
        fields = ['id', 'donor', 'donor_name', 'donor_blood_group', 'donor_phone',
                  'request_date', 'preferred_date', 'units', 'status', 
                  'admin_notes', 'approved_by', 'approved_date']
        read_only_fields = ['request_date', 'status', 'approved_by', 'approved_date']
    
    def validate(self, data):
        donor = data.get('donor')
        pending_exists = DonationRequest.objects.filter(
            donor=donor,
            status='pending'
        ).exists()
        
        if pending_exists:
            raise serializers.ValidationError(
                "You already have a pending donation request. Please wait for approval."
            )
        return data

class DonationRequestApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationRequest
        fields = ['status', 'admin_notes']
    
    def validate_status(self, value):
        if value not in ['approved', 'rejected', 'completed']:
            raise serializers.ValidationError("Invalid status")
        return value
