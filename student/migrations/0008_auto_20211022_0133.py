# Generated by Django 3.1.4 on 2021-10-21 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_user_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='branch',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='college',
            field=models.CharField(max_length=50),
        ),
    ]