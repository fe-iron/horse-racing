from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Registration(models.Model):
    referral = models.CharField(max_length=12, null=False)
    phone_number = models.IntegerField(blank=True, unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    balance = models.CharField(max_length=50, default="20")
    win_balance = models.CharField(max_length=50, default='0')

    def __str__(self):
        return self.full_name


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


class TransactionDetail(models.Model):
    made_by = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="Transaction_detail")
    transaction_id = models.CharField(max_length=255)
    bank_txn_id = models.CharField(max_length=255)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    gateway_name = models .CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=10)

    def __str__(self):
        return str(self.timestamp) + " " + str(self.transaction_id)


class HorseRacing(models.Model):
    game_no = models.IntegerField()
    open = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    horse1 = models.IntegerField(default=0)
    horse2 = models.IntegerField(default=0)
    horse3 = models.IntegerField(default=0)
    winner = models.CharField(max_length=10, default="No One")

    def __str__(self):
        return str(self.game_no)


class Player(models.Model):
    player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="player_name")
    timestamp = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(HorseRacing, on_delete=models.SET_NULL, null=True, related_name="game_name")
    bet_on = models.CharField(max_length=10, null=False)
    amount = models.IntegerField()
    result = models.CharField(max_length=10, default="Not Set")

    def __str__(self):
        return str(self.player)


# this model is for stroing history of users betting
class GamePointHistory(models.Model):
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField()
    made_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recharge_by")
    balance = models.IntegerField()

    def __str__(self):
        return str(self.amount)


class GamePlayHistory(models.Model):
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField()
    which_horse = models.CharField(max_length=20)
    result = models.CharField(max_length=10, default='Lose')
    game = models.ForeignKey(HorseRacing, on_delete=models.CASCADE, related_name="horse_history", default=None, null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player_history", default=None, null=True)

    def __str__(self):
        return self.which_horse
