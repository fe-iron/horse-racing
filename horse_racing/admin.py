from django.contrib import admin
from .models import Registration, Transaction, Referral, TransactionDetail, HorseRacing, Player, GamePlayHistory, \
    GamePointHistory, Subscriber, CommissionHistory
# Register your models here.

admin.site.register(Registration)
admin.site.register(Transaction)
admin.site.register(Referral)
admin.site.register(Subscriber)
admin.site.register(TransactionDetail)
admin.site.register(HorseRacing)
admin.site.register(Player)
admin.site.register(GamePlayHistory)
admin.site.register(CommissionHistory)
admin.site.register(GamePointHistory)