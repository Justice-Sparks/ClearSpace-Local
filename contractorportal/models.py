# contractorportal/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    """
    Custom user to allow future flexibility.
    For now, we keep username but enforce unique email.
    """
    email = models.EmailField(unique=True)

class ContractorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200, blank=True)
    contact_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    # Portal fields  
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to="contractor_photos/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name or self.user.email 