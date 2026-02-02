from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employer', 'Employer'),
        ('worker', 'Worker'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    skill = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)

    google_id = models.CharField(max_length=255, null=True, blank=True)
    oauth_provider = models.CharField(max_length=50, null=True, blank=True)
    is_oauth_complete = models.BooleanField(default=False)
    profile_picture = models.URLField(null=True, blank=True)
