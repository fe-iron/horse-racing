from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Registration(models.Model):
    referral = models.CharField(max_length=12, null=False)
    phone_number = models.IntegerField(blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Referral(models.Model):
    referral = models.CharField(max_length=10, default="DEFAULT000")
    created_on = models.DateTimeField()
    assign_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_for")
    created_by = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.referral
