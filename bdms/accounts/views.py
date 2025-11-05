from rest_framework import status, generics, permissions

from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response

from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate, login, logout, get_user_model

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from accounts.serializers import RegisterSerializer, DonorProfileSerializer, UserSerializer

from accounts.models import *

from accounts.forms import DonorRegistrationForm, DonorProfileForm



User = get_user_model()



@api_view(['POST'])

@permission_classes([permissions.AllowAny])

def register_api(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():

        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({

            'user': UserSerializer(user).data,

            'token': token.key

        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])

@permission_classes([permissions.AllowAny])

def login_api(request):

    username = request.data.get('username')

    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    

    if user:

        token, _ = Token.objects.get_or_create(user=user)

        return Response({

            'user': UserSerializer(user).data,

            'token': token.key

        })

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])

def logout_api(request):

    if request.user.is_authenticated:

        Token.objects.filter(user=request.user).delete()

    return Response({'message': 'Logged out successfully'})



class DonorProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = DonorProfileSerializer

    permission_classes = [permissions.IsAuthenticated]

    

    def get_object(self):

        return DonorProfile.objects.get(user=self.request.user)



class DonorListView(generics.ListAPIView):

    serializer_class = DonorProfileSerializer

    permission_classes = [permissions.IsAuthenticated]

    

    def get_queryset(self):

        queryset = DonorProfile.objects.all()

        blood_group = self.request.query_params.get('blood_group')

        is_available = self.request.query_params.get('is_available')

        

        if blood_group:

            queryset = queryset.filter(blood_group=blood_group)

        if is_available is not None:

            queryset = queryset.filter(is_available=is_available.lower() == 'true')

        

        return queryset

def register_view(request):

    if request.user.is_authenticated:

        return redirect('donor_dashboard')

    

    if request.method == 'POST':

        form = DonorRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(request, 'Registration successful!')

            return redirect('donor_dashboard')

    else:

        form = DonorRegistrationForm()

    

    return render(request, 'accounts/register.html', {'form': form})



def login_view(request):

    if request.user.is_authenticated:

        if request.user.is_admin:

            return redirect('admin_dashboard')

        return redirect('donor_dashboard')

    

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        

        if user:

            login(request, user)

            if user.is_admin:

                return redirect('admin_dashboard')

            return redirect('donor_dashboard')

        else:

            messages.error(request, 'Invalid credentials')

    

    return render(request, 'accounts/login.html')



@login_required

def logout_view(request):

    logout(request)

    messages.success(request, 'Logged out successfully')

    return redirect('login')



@login_required

def profile_view(request):

    if not request.user.is_donor:

        return redirect('admin_dashboard')

    

    profile = request.user.donor_profile

    

    if request.method == 'POST':

        form = DonorProfileForm(request.POST, instance=profile)

        if form.is_valid():

            form.save()

            messages.success(request, 'Profile updated successfully!')

            return redirect('profile')

    else:

        form = DonorProfileForm(instance=profile)

    

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})