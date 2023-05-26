# from django.shortcuts import render
# from rest_framework import  generics

# from rest_framework import generics, permissions
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework.settings import api_settings
# from .serializers import UserSerializer, UserProfileSerializer, AuthTokenSerializer
# from rest_framework.authentication import SessionAuthentication
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import logout

from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import UserProfile
# from .serializers import UserProfileSerializer

# from django.contrib.auth import logout
# from django.shortcuts import redirect

# class LogoutView(ObtainAuthToken):
#     def post(self, request):
#         # Delete the user's authentication token
#         Token.objects.filter(user=request.user).delete()
#         return Response({'detail': 'Logged out successfully'})


# class CustomList(generics.ListCreateAPIView):
#     # authentication_classes = [SessionAuthentication]
#     # permission_classes = [IsAuthenticated]
#     pass


# class CustomDetail(generics.RetrieveDestroyAPIView):
#     pass

# class ProfileAPIView(APIView):
#     # authentication_classes = [SessionAuthentication]
#     # permission_classes = [IsAuthenticated]
#     queryset = UserProfile.objects.all()

#     def get(self, request):
#         try:
#             profile = UserProfile.objects.get(user=request.user)
#             # print(request.user.username)
#             serializer = UserProfileSerializer(profile)
#             return Response(serializer.data)
#         except UserProfile.DoesNotExist:
#             return Response({'error': 'Profile not found.'}, status=404)

# # class CreateUserView(generics.CreateAPIView):
# #     serializer_class = UserSerializer
# #     permission_classes = (permissions.AllowAny,)


# class CreateTokenView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         # Logout any authenticated user
#         logout(request)
        
#         # Check the user's account type
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         print(user,request.data['group'])
        
#         # Handle different account types
#         if user.is_staff:
#             if request.data['group'] == 'admin':
#                 # Perform user-specific authentication logic
#                 return Response({'token': token.key, 'account_type': 'admin'})
#             else:
#                 return Response({'detail': 'Invalid account type'}, status=400)
#         else:
#             if request.data['group'] == 'user':
#                 # Perform admin-specific authentication logic
#                 return Response({'token': token.key, 'account_type': 'user'})
#             else:
#                 return Response({'detail': 'Invalid account type'}, status=400)

from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from .models import *
from .serializers import *


class LogoutView(ObtainAuthToken):
    def post(self, request):
        # Delete the user's authentication token
        Token.objects.filter(user=request.user).delete()
        return Response({'detail': 'Logged out successfully'})


class CustomList(generics.ListCreateAPIView):
    pass


class CustomDetail(generics.RetrieveDestroyAPIView):
    pass


# class ProfileAPIView(generics.ListAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#     # authentication_classes = [SessionAuthentication]
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         profile = UserProfile.objects.filter(user=user)[0]
#         print(user, profile.first_name,  profile.last_name)
#         return profile


# class CreateTokenView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         # Logout any authenticated user
#         logout(request)

#         # Check the user's account type
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)

#         # Handle different account types
#         if user.is_staff:
#             if request.data['group'] == 'admin':
#                 # Perform user-specific authentication logic
#                 return Response({'token': token.key, 'account_type': 'admin'})
#             else:
#                 return Response({'detail': 'Invalid account type'}, status=400)
#         else:
#             if request.data['group'] == 'user':
#                 # Perform admin-specific authentication logic
#                 return Response({'token': token.key, 'account_type': 'user'})
#             else:
#                 return Response({'detail': 'Invalid account type'}, status=400)

class ProfileAPIView(APIView):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            # print(request.user.username)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found.'}, status=404)

class CreateTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Logout any authenticated user
        logout(request)
        
        # Check the user's account type
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print(user,request.data['group'])
        
        # Handle different account types
        if user.is_superuser:
            if request.data['group'] == 'admin':
                # Perform user-specific authentication logic
                return Response({'token': token.key, 'account_type': 'admin'})
            else:
                return Response({'detail': 'Invalid account type'}, status=400)
        elif user.is_staff:
            if request.data['group'] == 'admin':
                # Perform user-specific authentication logic
                return Response({'token': token.key, 'account_type': 'staff'})
            else:
                return Response({'detail': 'Invalid account type'}, status=400)
        else:
            if request.data['group'] == 'user':
                # Perform admin-specific authentication logic
                return Response({'token': token.key, 'account_type': 'user'})
            else:
                return Response({'detail': 'Invalid account type'}, status=400)


class CountyList(generics.ListCreateAPIView):
    queryset = County.objects.all()[:50]
    serializer_class = CountySerializer


class CountyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = County.objects.all()[:50]
    serializer_class = CountySerializer


class ConstituencyList(generics.ListCreateAPIView):
    queryset = Constituency.objects.all()[:50]
    serializer_class = ConstituencySerializer


class ConstituencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Constituency.objects.all()[:50]
    serializer_class = ConstituencySerializer


class WardList(generics.ListCreateAPIView):
    queryset = Ward.objects.all()[:50]
    serializer_class = WardSerializer


class WardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ward.objects.all()[:50]
    serializer_class = WardSerializer


class PollingCenterList(generics.ListCreateAPIView):
    queryset = PollingCenter.objects.all()[:50]
    serializer_class = PollingCenterSerializer


class PollingCenterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PollingCenter.objects.all()[:50]
    serializer_class = PollingCenterSerializer


class PollingStationList(generics.ListCreateAPIView):
    queryset = PollingStation.objects.all()[:50]
    serializer_class = PollingStationSerializer


class PollingStationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PollingStation.objects.all()[:50]
    serializer_class = PollingStationSerializer


class QueueList(generics.ListCreateAPIView):
    queryset = Queue.objects.all()[:50]
    serializer_class = QueueSerializer


class QueueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Queue.objects.all()[:50]
    serializer_class = QueueSerializer


class VoterList(generics.ListCreateAPIView):
    queryset = Voter.objects.all()[:50]
    serializer_class = VoterSerializer


class VoterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voter.objects.all()[:50]
    serializer_class = VoterSerializer


class StaffList(generics.ListCreateAPIView):
    queryset = Staff.objects.all()[:50]
    serializer_class = StaffSerializer


class StaffDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()[:50]
    serializer_class = StaffSerializer


class TicketList(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()[:50]
    serializer_class = TicketSerializer


class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()[:50]
    serializer_class = TicketSerializer


class TimeSlotList(generics.ListCreateAPIView):
    queryset = TimeSlot.objects.all()[:50]
    serializer_class = TimeSlotSerializer


class TimeSlotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TimeSlot.objects.all()[:50]
    serializer_class = TimeSlotSerializer


class VoteList(generics.ListCreateAPIView):
    queryset = Vote.objects.all()[:50]
    serializer_class = VoteSerializer


class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()[:50]
    serializer_class = VoteSerializer
