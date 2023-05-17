from django.shortcuts import render
from rest_framework import  generics


class CustomList(generics.ListCreateAPIView):
    pass


class CustomDetail(generics.RetrieveDestroyAPIView):
    pass