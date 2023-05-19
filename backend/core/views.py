from django.shortcuts import render
from rest_framework import  generics

from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from .serializers import UserSerializer, UserProfileSerializer, AuthTokenSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer

from django.contrib.auth import logout
from django.shortcuts import redirect

class LogoutView(ObtainAuthToken):
    def post(self, request):
        # Delete the user's authentication token
        Token.objects.filter(user=request.user).delete()
        return Response({'detail': 'Logged out successfully'})


class CustomList(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class CustomDetail(generics.RetrieveDestroyAPIView):
    pass

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

# class CreateUserView(generics.CreateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = (permissions.AllowAny,)


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
        if user.is_staff:
            if request.data['group'] == 'admin':
                # Perform user-specific authentication logic
                return Response({'token': token.key, 'account_type': 'admin'})
            else:
                return Response({'detail': 'Invalid account type'}, status=400)
        else:
            if request.data['group'] == 'user':
                # Perform admin-specific authentication logic
                return Response({'token': token.key, 'account_type': 'user'})
            else:
                return Response({'detail': 'Invalid account type'}, status=400)