# Generated by Django 3.2.1 on 2021-05-15 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('horse_racing', '0005_auto_20210513_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='txn',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_txn', to='horse_racing.transaction'),
        ),
    ]
