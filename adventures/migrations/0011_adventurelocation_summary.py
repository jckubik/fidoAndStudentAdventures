# Generated by Django 3.2.8 on 2021-12-01 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventures', '0010_adventuretrip_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventurelocation',
            name='summary',
            field=models.TextField(default=''),
        ),
    ]
