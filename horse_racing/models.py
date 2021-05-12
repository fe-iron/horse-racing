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
    created_on = models.DateTimeField(auto_now_add=True)
    assign_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_for")
    created_by = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.referral


class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id