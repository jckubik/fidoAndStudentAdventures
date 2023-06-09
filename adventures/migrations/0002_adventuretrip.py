# Generated by Django 3.2.8 on 2021-10-25 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventures', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdventureTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('author', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('alt', models.CharField(max_length=100)),
            ],
        ),
    ]
