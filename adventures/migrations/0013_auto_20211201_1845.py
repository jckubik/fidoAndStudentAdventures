# Generated by Django 3.2.8 on 2021-12-01 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventures', '0012_adventuretrip_adventurelocation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adventuretrip',
            name='alt',
        ),
        migrations.RemoveField(
            model_name='adventuretrip',
            name='img',
        ),
        migrations.AddField(
            model_name='adventuretrip',
            name='summary',
            field=models.TextField(default=''),
        ),
    ]
