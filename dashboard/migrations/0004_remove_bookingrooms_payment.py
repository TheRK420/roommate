# Generated by Django 3.2.6 on 2021-10-19 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20211019_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingrooms',
            name='payment',
        ),
    ]
