# Generated by Django 3.1.4 on 2021-10-26 16:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_auto_20211026_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingrooms',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 26, 22, 3, 49, 759912)),
        ),
    ]
