from unittest.util import _MAX_LENGTH
from rest_framework import serializers
#from challenges import models
from . import models
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    """serializes a user profile object """

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True, 'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """create a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        return user


class ProfilePostsItemSerializer(serializers.ModelSerializer):
    """Serializes Posts Tags"""

    class Meta:
        model = models.Posts
        fields = ('id', 'title', 'description','image','tag',)
        extra_kwargs = {'user_profile': {'read_only': True}}



class ProfileTagsItemSerializer(serializers.ModelSerializer):
    """Serializes profile posts"""

    class Meta:
        model = models.tags
        fields = ('id', 'tag')
        #extra_kwargs = {'user_profile': {'read_only': True}}

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)