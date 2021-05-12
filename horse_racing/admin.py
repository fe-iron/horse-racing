from django.contrib import admin
from .models import Registration, Transaction, Referral
# Register your models here.

admin.site.register(Registration)
admin.site.register(Transaction)
admin.site.register(Referral)
