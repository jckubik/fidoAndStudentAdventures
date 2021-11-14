# Generated by Django 3.2.8 on 2021-10-25 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventures', '0004_alter_adventurelocation_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adventurelocation',
            name='num_reviews',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='adventuretrip',
            name='date',
            field=models.DateTimeField(),
        ),
    ]