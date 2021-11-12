# Generated by Django 3.2.6 on 2021-09-17 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=40)),
                ('Phone', models.CharField(max_length=20)),
                ('Subject', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Dataform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=30)),
                ('Contact', models.CharField(max_length=30)),
                ('Photo', models.FileField(null=True, upload_to='media/')),
                ('Aadhar', models.FileField(null=True, upload_to='media/')),
                ('PanCard', models.FileField(null=True, upload_to='media/')),
                ('Service', models.CharField(max_length=30)),
                ('hostel_name', models.CharField(max_length=30)),
                ('hcontact', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=30)),
                ('capacity', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=30)),
                ('facilities', models.CharField(max_length=100, null=True)),
                ('property', models.FileField(null=True, upload_to='media/')),
                ('completion', models.FileField(null=True, upload_to='media/')),
                ('permission', models.FileField(null=True, upload_to='media/')),
                ('proof', models.FileField(null=True, upload_to='media/')),
                ('regist', models.FileField(null=True, upload_to='media/')),
                ('staff', models.CharField(max_length=30)),
                ('distance', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=40)),
                ('email', models.CharField(max_length=40)),
                ('town', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=50)),
                ('is_registered', models.BooleanField()),
            ],
        ),
    ]
