from django.db import models
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_init
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your models here.
class User(models.Model):
    Name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=30)
    is_registered=models.BooleanField()
    vendor=models.BooleanField(default=False)


    def __str__(self):
        return self.Name



class Dataform(models.Model):
    Name = models.CharField(max_length=50, null=True)
    Contact =models.CharField(max_length=30)
    Photo=models.FileField(upload_to='media/', null=True)
    Aadhar=models.FileField(upload_to='media/', null=True)
    PanCard=models.FileField(upload_to='media/', null=True)
    Service=models.CharField(max_length=30)
    hostel_name=models.CharField(max_length=50, null=True)
    hcontact =models.CharField(max_length=30, null=True)
    address=models.CharField(max_length=100, null=True)
    capacity=models.CharField(max_length=30)
    category=models.CharField(max_length=30)
    facilities=models.CharField(max_length=100, null=True)
    property=models.FileField(upload_to='media/', null=True)
    completion=models.FileField(upload_to='media/', null=True)
    hostel_photo=models.FileField(upload_to='media/', null=True)
    permission=models.FileField(upload_to='media/', null=True)
    proof=models.FileField(upload_to='media/', null=True)
    regist=models.FileField(upload_to='media/', null=True)
    staff=models.CharField(max_length=30)
    distance=models.CharField(max_length=30)
    email=models.CharField(max_length=50)
    Verified=models.BooleanField(default=False)

    def save(self):
        if self.id:
            print("Hi")
            old_foo = Dataform.objects.get(pk=self.id)
            if old_foo.Verified == False:
                print("Not V")
                email_subject = 'Roommate KYC Verified'
                # email_body = '''Respected sir/ma'am,

                # Your document KYC with a roommate has been successfully completed,
                # we welcome you to our Techmihirnaik family and would be honored to work with you.

                # you will receive the link for the dashboard soon.


                # Regards,
                # techmihirnaik'''
                html_message = render_to_string('roommate/KYCmail.html', {
                    'user':old_foo
                })
                email_body = strip_tags(html_message)
                # email = EmailMessage(subject=email_subject, body=email_body,
                #                      from_email=settings.EMAIL_FROM_USER,
                #                      to=[old_foo.email]
                #                      )
                msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [old_foo.email])
                msg.attach_alternative(html_message, "text/html")
                # print('HIII')
                msg.send()
        super(Dataform, self).save()


    def __str__(self):
        return self.Name



class ContactUs(models.Model):
    Name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    Phone = models.CharField(max_length=20)
    Subject= models.CharField(max_length=100)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.Name


