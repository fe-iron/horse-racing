# Generated by Django 3.2.1 on 2021-05-17 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horse_racing', '0016_gameplayhistory_total_bet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=25)),
            ],
        ),
    ]
