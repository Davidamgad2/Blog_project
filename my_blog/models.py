from email.policy import default
from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


# Create your models here.

class UserProfileManager(BaseUserManager):
    """Handling user logins"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have email address and name")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """create and save a new super user with given details"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Handling user profiles"""
    email = models.CharField(max_length=225, unique=True)
    name = models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """retrieve full name of user"""
        return self.name

    def __str__(self):
        """return string represent of our user"""
        return self.email
        
    def get_id(self):
        current_user = self.user

        return current_user.id

class tags():
    """tags for blogs"""
    tag=models.CharField(max_length=255)

    def __str__(self):
        """return string represent the tag"""
        return self.tag


class Posts():
    """ blogs' content """
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title=models.CharField(max_length=255)
    description = models.CharField(max_length=15000)
    image=models.ImageField(upload_to='images')
    tag=tags()
    user_id=UserProfile()
    created_on = models.DateTimeField(auto_now_add=True)
