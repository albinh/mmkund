# Generated by Django 3.0.2 on 2020-01-26 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kunder', '0009_auto_20200125_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=255, verbose_name='e-post'),
        ),
    ]