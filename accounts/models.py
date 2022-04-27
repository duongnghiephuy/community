from email.headerregistry import Group
from django.db import models
from django.contrib.auth.models import User, Group


class UserProfile(models.Model):
    email = models.EmailField(blank=True)
    fullname = models.CharField(max_length=100, blank=True)
    address = models.TextField(max_length=300, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


