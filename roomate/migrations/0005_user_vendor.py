# Generated by Django 3.2.6 on 2021-10-06 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomate', '0004_remove_dataform_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='vendor',
            field=models.BooleanField(default=False),
        ),
    ]