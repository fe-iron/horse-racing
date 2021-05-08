from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Registration(models.Model):
    referral = models.CharField(max_length=12, null=False)
    phone_number = models.IntegerField(blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
