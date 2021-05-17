# Generated by Django 3.2.1 on 2021-05-17 10:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('horse_racing', '0018_transactiondetail_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='assign_to',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_for', to=settings.AUTH_USER_MODEL),
        ),
    ]
