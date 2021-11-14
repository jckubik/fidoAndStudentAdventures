# Generated by Django 3.2.8 on 2021-11-02 19:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adventures', '0007_auto_20211101_2222'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=30)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('review', models.TextField()),
                ('rating', models.FloatField(default=5)),
                ('adventureLocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adventures.adventurelocation')),
            ],
        ),
    ]