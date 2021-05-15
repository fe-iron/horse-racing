# Generated by Django 3.2.1 on 2021-05-13 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('horse_racing', '0003_auto_20210512_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='HorseRacing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_no', models.IntegerField()),
                ('open', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('horse1', models.IntegerField()),
                ('horse2', models.IntegerField()),
                ('horse3', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TransactionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=255)),
                ('bank_txn_id', models.CharField(max_length=255)),
                ('currency', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('gateway_name', models.CharField(max_length=50)),
                ('bank_name', models.CharField(max_length=100)),
                ('bin_name', models.CharField(max_length=100)),
                ('payment_mode', models.CharField(max_length=10)),
                ('made_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Transaction_detail', to='horse_racing.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('bet_on', models.CharField(max_length=10)),
                ('amount', models.IntegerField()),
                ('result', models.CharField(default='Not Set', max_length=10)),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_name', to='horse_racing.horseracing')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]