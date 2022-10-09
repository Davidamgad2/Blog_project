from django.shortcuts import render
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.urls import include, path,reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from .serializer import ChangePasswordSerializer

from . import serializer, models, permissions

# Create your views here.

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    
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

#model view set bydeny al list create update 

class UserProfileTagsViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializer.ProfileTagsItemSerializer

    queryset = models.tags.objects.all()

    permission_classes = (
        permissions.updateownprofile,
        IsAuthenticated
    )

    # def perform_create(self, serializer):
    #     """Sets the user profile to the logged in user"""
    #     serializer.save(user_profile=self.request.user)
       

    # def update(self, request, pk=None):
    #     """Handle and updating object"""
    #     return Response({'http_method': 'PUT'})


    # def destroy(self, request, pk=None):
    #     """handling destroy the object"""
    #     return Response({'http_method': 'Delete'})
    

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
    
    # 34an al override kdh lw ana sbt ali t7t dol uncommented 
    
    # def retrieve(self, request, pk=None):
    #     """handle getting an object by its id """
    #     return Response({'http_method': 'GET'})

    # def update(self, request, pk=None):
    #     """Handle and updating object"""
    #     return Response({'http_method': 'PUT'})

    # def partial_update(self, request, pk=None):
    #     """handling partial update for the object"""
    #     return Response({'http_method': 'Patch'})

    # def destroy(self, request, pk=None):
    #     """handling destroy the object"""
    #     return Response({'http_method': 'Delete'})
    
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)