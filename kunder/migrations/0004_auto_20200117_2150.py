# Generated by Django 3.0.2 on 2020-01-17 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kunder', '0003_auto_20200117_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='even',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='odd',
            field=models.BooleanField(default=False),
        ),
    ]
