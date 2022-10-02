from django.shortcuts import render
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.urls import include, path
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from . import serializer, models, permissions

# Create your views here.


class UserProfileViewSet(viewsets.ModelViewSet):
    """handle creating and updating profiles """
    serializer_class = serializer.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    # how the user will auth the mechanism and permission says how the user gets permission to do the certain things
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.updateownprofile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class userloginapiview(ObtainAuthToken):
    """handling  creating user auth token """

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileTagsViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializer.ProfileTagsItemSerializer

    queryset = models.tags.objects.all()
    permission_classes = (
        permissions.updateownprofile,
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
       

    def update(self, request, pk=None):
        """Handle and updating object"""
        return Response({'http_method': 'PUT'})


    def destroy(self, request, pk=None):
        """handling destroy the object"""
        return Response({'http_method': 'Delete'})
    

class UserProfilePostsViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializer.ProfilePostsItemSerializer
    queryset = models.Posts.objects.all()
    permission_classes = (
        permissions.updateownprofile,
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
    
    
    def retrieve(self, request, pk=None):
        """handle getting an object by its id """
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle and updating object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """handling partial update for the object"""
        return Response({'http_method': 'Patch'})

    def destroy(self, request, pk=None):
        """handling destroy the object"""
        return Response({'http_method': 'Delete'})