from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    A custom user model based on AbstractUser, using email as the unique identifier.
    """ 
    username = None   
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # Define the field Django should use for authentication
    USERNAME_FIELD = 'email'
    # Define fields required when creating a superuser from the command line
    REQUIRED_FIELDS = ['full_name'] 
    def __str__(self):
        return self.email