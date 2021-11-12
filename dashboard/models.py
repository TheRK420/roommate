from django.db import models
from django.core.mail import EmailMessage
from django.db.models.signals import post_save, post_init
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives



import uuid
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models


# Create your models here.
class addroom(models.Model):
    description=models.CharField(max_length=3000)
    email=models.CharField(max_length=50)
    category=models.CharField(max_length=30)
    hostel_name=models.CharField(max_length=50)
    num_room=models.CharField(max_length=10,default=0)
    discount=models.CharField(max_length=30)
    gender=models.CharField(max_length=30,default="UniSex")
    price=models.CharField(max_length=30)
    month=models.CharField(max_length=30,default="1 month")
    image1=models.FileField(upload_to='media/')
    # image1=models.ImageField(upload_to='media/',height_field=50, width_field=50)
    image2=models.FileField(upload_to='media/')
    image3=models.FileField(upload_to='media/')
    image4=models.FileField(upload_to='media/')
    image5=models.FileField(upload_to='media/')
    image6=models.FileField(upload_to='media/')
    date=models.CharField(max_length=15)
    Restaurant=models.BooleanField(default=False)
    CarBus=models.BooleanField(default=False)
    Stationary=models.BooleanField(default=False)
    BikeRent=models.BooleanField(default=False)
    Wifi=models.BooleanField(default=False)
    Laundry=models.BooleanField(default=False)
    Gym=models.BooleanField(default=False)
    Water=models.BooleanField(default=False)
    CCTV=models.BooleanField(default=False)
    verified=models.BooleanField(default=False)
    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         self.resize(self.image1, (50, 50))
    #         self.resize(self.image2, (50, 50))
    #         self.resize(self.image3, (50, 50))
    #         self.resize(self.image4, (50, 50))
    #         self.resize(self.image5, (50, 50))
    #         self.resize(self.image6, (50, 50))

    #     super().save(*args, **kwargs)
    # def resize(self, imageField: models.ImageField, size:tuple):
    #     im = Image.open(imageField)  # Catch original
    #     source_image = im.convert('RGB')
    #     source_image.thumbnail(size)  # Resize to size
    #     output = BytesIO()
    #     source_image.save(output, format='JPEG') # Save resize image to bytes
    #     output.seek(0)

    #     content_file = ContentFile(output.read())  # Read output and create ContentFile in memory
    #     file = File(content_file)

    #     random_name = f'{uuid.uuid4()}.jpeg'
    #     print(random_name)
    #     imageField.save(random_name, file, save=False)

    def __str__(self):
        return self.hostel_name+'_'+self.category





# from datetime import date
from django.utils import timezone
from datetime import date


class bookingrooms(models.Model):
    timestamp = models.DateTimeField(default=date.today())
    booking_id=models.CharField(max_length=30,default=0)
    logged_mail=models.CharField(max_length=50,default='null')
    cust_name=models.CharField(max_length=50,default='null')
    category=models.CharField(max_length=30,default='null')
    hostel_name=models.CharField(max_length=50,default='null')
    gender=models.CharField(max_length=30,default='null')
    email=models.CharField(max_length=50,default='null')
    contact=models.CharField(max_length=30,default='null')
    college=models.CharField(max_length=100,default='null')
    branch=models.CharField(max_length=30,default='null')
    date=models.CharField(max_length=30,default='null')
    city=models.CharField(max_length=30,default='null')
    year=models.CharField(max_length=30,default='null')
    duration=models.CharField(max_length=30,default='null')
    total=models.CharField(max_length=30,default='null')
    confirmation=models.BooleanField(default=False)
    payment=models.BooleanField(max_length=30,default='0')
    reg_payment=models.BooleanField(max_length=30,default='0')
    rejected=models.BooleanField(default=False)

    def __str__(self):
        return self.cust_name

    '''def save(self):
        if self.id:
            print("Hi")
            old_foo = bookingrooms.objects.get(pk=self.id)
            print(old_foo.email)
            if old_foo.confirmation == True:
                print("Not V")
                email_subject = 'KYC Verified'
                email_body = Respected sir/ma'am,

                Your document KYC with a roommate has been successfully completed,
                we welcome you to our Techmihirnaik family and would be honored to work with you.

                you will receive the link for the dashboard soon.


                yours sincerely,
                Karthik
                html_message = render_to_string('roommate/single-news.html')
                email_body = strip_tags(html_message)
                #email = EmailMessage(subject=email_subject, body=email_body,
                                     #from_email=settings.EMAIL_FROM_USER,
                                     #to=[old_foo.email]
                                     #)
                msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [old_foo.email])
                msg.attach_alternative(html_message, "text/html")
                print('HIII')
                msg.send()
            if(old_foo.confirmation==False and old_foo.reg_payment==True):
                pass
        super(bookingrooms, self).save()'''



class payment_link(models.Model):
    cust_name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    logged_mail=models.CharField(max_length=50,default="")
    hostel_name=models.CharField(max_length=50)
    category=models.CharField(max_length=30)
    amount=models.CharField(max_length=30)
    gender=models.CharField(max_length=20,default="UniSex")
    orderid=models.CharField(max_length=30,default="")
    transaction_id999=models.CharField(max_length=50,default="")
    transaction_id_full=models.CharField(max_length=50,default="")
    payment_mode999=models.CharField(max_length=50,default="")
    payment_modefull=models.CharField(max_length=50,default="")
    transaction_date999=models.CharField(max_length=50,default="")
    transaction_datefull=models.CharField(max_length=50,default="")
    bank_transaction_id999=models.CharField(max_length=50,default="")
    bank_transaction_idfull=models.CharField(max_length=50,default="")
    bank_name999=models.CharField(max_length=50,default="")
    bank_namefull=models.CharField(max_length=50,default="")
    
    
    def __str__(self):
        return self.cust_name+" "+self.hostel_name+" "+self.category