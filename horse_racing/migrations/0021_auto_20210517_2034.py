# Generated by Django 3.2.1 on 2021-05-17 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horse_racing', '0020_auto_20210517_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commissionhistory',
            name='date',
        ),
        migrations.RemoveField(
            model_name='commissionhistory',
            name='time',
        ),
        migrations.AddField(
            model_name='commissionhistory',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
