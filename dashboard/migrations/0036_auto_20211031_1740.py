# Generated by Django 3.1.4 on 2021-10-31 12:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0035_auto_20211031_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment_link',
            name='gender',
        ),
        migrations.AddField(
            model_name='payment_link',
            name='bank_name999',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='payment_link',
            name='bank_namefull',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='payment_link',
            name='bank_transaction_id999',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='payment_link',
            name='bank_transaction_idfull',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='payment_link',
            name='logged_mail',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='payment_link',
            name='orderid',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='payment_link',
            name='payment_mode999',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='payment_link',
            name='payment_modefull',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='payment_link',
            name='transaction_date999',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='payment_link',
            name='transaction_datefull',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='payment_link',
            name='transaction_id999',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='payment_link',
            name='transaction_id_full',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='bookingrooms',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 17, 40, 34, 768874)),
        ),
    ]
