from django.db import models
from django.conf import settings

# Create your models here.
class User(models.Model):
    student_id= models.CharField(max_length=30,default=0)
    Name= models.CharField(max_length=50)
    photo= models.FileField(upload_to='media/', null=True)
    aadhar= models.FileField(upload_to='media/', null=True)
    contact= models.CharField(max_length=30)
    email= models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    college= models.CharField(max_length=50)
    branch= models.CharField(max_length=50)
    year= models.CharField(max_length=30)

    def __str__(self):
        return self.email



class Reviews(models.Model):
    email= models.CharField(max_length=50)
    hostel_name=models.CharField(max_length=50)
    category=models.CharField(max_length=30)
    gender=models.CharField(max_length=10,default="UniSex")
    Quality=models.CharField(max_length=10)
    Location=models.CharField(max_length=10)
    Space=models.CharField(max_length=10)
    Service=models.CharField(max_length=10)
    Price=models.CharField(max_length=10)
    def __str__(self):
        return self.hostel_name+"_"+self.category
    
    
class comments(models.Model):
    student_name=models.CharField(max_length=40)
    gender=models.CharField(max_length=10,default="Boys")
    comment=models.CharField(max_length=100)
    hostel_name=models.CharField(max_length=50,default="")
    category=models.CharField(max_length=30)
    date_comment=models.CharField(max_length=40)
    email_vendor=models.CharField(max_length=100)
    published=models.BooleanField(default=False)


    def __str__(self):
        return  self.student_name