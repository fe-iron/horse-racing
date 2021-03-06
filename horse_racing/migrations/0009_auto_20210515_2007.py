# Generated by Django 3.2.1 on 2021-05-15 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('horse_racing', '0008_auto_20210515_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamePlayHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('which_horse', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='player',
            name='txn',
        ),
        migrations.CreateModel(
            name='RechargeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('made_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recharge_by', to=settings.AUTH_USER_MODEL)),
                ('txn_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='txn_history', to='horse_racing.transaction')),
            ],
        ),
    ]
