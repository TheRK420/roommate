

from django.http import response
from django.http.response import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from roomate.models import  ContactUs, Dataform, User
from django.contrib.auth import login, authenticate, logout
from datetime import datetime
from django.contrib.auth import get_user_model
import sqlite3
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import sqlite3
from dashboard.models import *
import json
import requests
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import urllib
import urllib.request
from main.settings import GOOGLE_RECAPTCHA_SECRET_KEY



def home(request):
    return render(request, 'roommate/index.html')


def listing(request):
    try:
        email = request.session['email']
        user = User.objects.get(email=email)
        return render(request, 'roommate/add-listing.html', context={'user': user})
    except:
        return redirect(signup)


def terms(request):
    return render(request, 'roommate/terms.html')


def policy(request):
    return render(request, 'roommate/policy.html')


def bookingpolicy(request):
    return render(request, 'roommate/bookingpolicy.html')


def register(request):
    try:
        status = request.session['status']
        return render(request, 'roommate/register.html', context={'status': status})
    except:
        return render(request, 'roommate/register.html')


def homepage(request):
    try:
        x = request.session['x']
        if x:
            email=request.session['email']
            user = User.objects.get(email=email)
            if(user.vendor):
                return render(request, 'roommate/home.html')
            else:
                listofroom= Dataform.objects.filter(Verified=True)[:3]
                print(listofroom)
                print(x)
                return render(request, 'Website/HOME.html', context={'x': x,'room':listofroom})
        else:
            return render(request, 'roommate/index.html')
    except:
        return render(request, 'roommate/index.html')

def adding_contact(request):
    if(request.method=='POST'):
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        subject=request.POST.get("subject")
        message=request.POST.get("message")
        recaptcha_response = request.POST.get('g-recaptcha-response')
        a=ContactUs(Name=name,email=email,Phone=phone,Subject=subject,message=message)
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
            }

        r = requests.post(url,data=values)
        result= r.json()
        
        if result['success']:
            a.save()
            print("SUCESS")
            messages.success(request, 'New comment added with success!')
        else:
            print("NO SUCCESS")
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        return redirect(contact)
    return render(request, 'roommate/contact-us.html')



def contact(request):
    try:
        x = request.session['x']
        if x:
            email = request.session['email']
            user = User.objects.get(email=email)
            print(x)
            return render(request, 'roommate/contact-us.html', context={'user': user, 'x': x})
        else:
            return render(request, 'roommate/contact-us.html')
    except:
        return render(request, 'roommate/contact-us.html')


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    html_message = render_to_string('roommate/registration_mail.html', {
        'user': user,
        'domain': current_site,
        'uid': user.email,
        'token': generate_token.make_token(user)
    })
    email_body = strip_tags(html_message)
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [user.email])
    msg.attach_alternative(html_message, "text/html")
    msg.send()


def activate_user(request, uidb64, token):
    
    user = User.objects.get(email=uidb64)
    user.is_registered = True
    user.save()
    request.session['status']='Email Verified!!'
    return redirect(register)


def signup(request):
    if request.method == 'POST':
        name = request.POST['dzName']
        email = request.POST['dzemail']
        addres = request.POST['dzadd']
        Town = request.POST['dztown']
        UserName = request.POST['dzUName']
        Password = request.POST['dzP']
        Rpassword = request.POST['dzrp']
        vendor=request.POST.get('vendor')
        if Password != Rpassword : 
            request.session['status']='Password does not match!!'
            return redirect(register)

        try:
            User.objects.get(email=email)
            request.session['status'] = 'Email Already Taken!!'
            return redirect(register)
        
        except:
            try:
                User.objects.get(username=UserName)
                request.session['status']='Username Already Taken'
                return redirect(register)
            
            
            except:
                if(vendor=='on'):
                    data = User(Name=name, address=addres, email=email,town=Town, username=UserName, password=Password,vendor=True)
                else:
                    data = User(Name=name, address=addres, email=email,town=Town, username=UserName, password=Password,vendor=False)
                data.is_registered = 0
                send_activation_email(data, request)
                data.save()
                request.session['status'] = 'Email sent!!...Please Verify it!'
                return redirect(register)

    return render(request, 'roommate/register.html')

def vendorHome(request):
    return render(request, 'roommate/home.html')

def user_login(request):

    if request.method == 'POST':
        data = request.POST
        username = request.POST.get('Name')
        password = request.POST.get('dzPa')
        print(len(username))
        try:
            user = User.objects.get(username=username)
            request.session['email'] = user.email
            if not user.is_registered:
                return render(request, "roommate/register.html", {"status": "Please Verify Your Account!!"})

            else:
                if password == user.password:
                    x = True
                    request.session['x'] = True
                    if(user.vendor):
                        return redirect('vendorHome')
                    else:
                        
                        return redirect(studentHome)
                else:
                    return render(request, "roommate/register.html", {"status": "Invalid Username or Password"})
        except User.DoesNotExist:
            return render(request, "roommate/register.html", {"status": "Invalid Username or Password"})

    return redirect(homepage)



def studentHome(request):
    listofroom= Dataform.objects.filter(Verified=True)[:3]
    return render(request, 'Website/HOME.html',context={'x':request.session['x'],'room':listofroom})



def user_logout(request):
    request.session['x'] = False
    logout(request)
    return redirect(home)


def forgot_mail(request):
    print(request.POST)
    e=request.POST['dzeM']
    user=User.objects.get(email=e)
    current_site = get_current_site(request)
    email_subject = 'Reset Your Password'
    html_message = render_to_string('roommate/ForgetNewMail.html', {
        'user': user,
        'domain': current_site,
        'uid': e,
        'token': generate_token.make_token(user)
    })
    email_body = strip_tags(html_message)
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [user.email])
    msg.attach_alternative(html_message, "text/html")
    msg.send()



def forgot_verify(request, email):
    request.session['e'] = email
    request.session['status'] = ''
    user = User.objects.get(email=email)
    return redirect('newpassword')


def trypass(request):
    email = request.session['e']
    status = request.session['status']
    return render(request, 'roommate/try.html', context={'status': status, 'm': email})


def Resetpass(request):
    if request.method == 'POST':
        try:
            print(request.POST)
            forgot_mail(request)
            return render(request, 'roommate/register.html', {'status': 'Please Check your mail to reset your password'})
        except:
            return render(request, 'roommate/register.html', {'status': 'Email Not Registered with us'})


def setpass(request, m):
    if request.method == 'POST':
        np = request.POST['np']
        rnp = request.POST['rnp']
        u = User.objects.get(email=m)
        if np == rnp:
            u.password = np
            u.save()
            request.session['status'] = 'Password Reset Successfully'
            return redirect(register)
        else:
            request.session['status'] = 'Please enter same password'
            return redirect('newpassword')


def dataofuser(request):
    if request.method == 'POST':
        email = request.session['email']
        Name = request.POST['Oname']
        Contact = request.POST['Ocontact']
        OPhoto = request.FILES.get('Ophoto')
        Oadhar = request.FILES.get('Oadhar')
        Opan = request.FILES.get('Opan')
        drop = request.POST['drop']
        Hname = request.POST['Hname']
        contact = request.POST['Contact']
        Haddress = request.POST['Haddress']
        capacity = request.POST['Capacity']
        gender = request.POST['gender']
        Moreinfo = request.POST['more']
        regisPaper = request.FILES.get('Regis')
        per = request.FILES.get('permission')
        hos = request.FILES.get('hostel')
        com = request.FILES.get('Completion')
        proof = request.FILES.get('proof')
        pproperty = request.FILES.get('property')
        staff = request.POST['staff']
        distance = request.POST['distance']
        detail = Dataform(Name=Name, Contact=Contact, Photo=OPhoto, Aadhar=Oadhar, PanCard=Opan, Service=drop, hostel_name=Hname, hcontact=contact, address=Haddress, capacity=capacity,category=gender, facilities=Moreinfo,hostel_photo=hos, property=pproperty, proof=proof, permission=per, completion=com, regist=regisPaper, staff=staff, distance=distance, email=email)
        detail.save()
        return redirect('kyc')
    return render(request, 'roommate/index.html')


def kyc(request):
    try:
        email = request.session['email']
        a = False
        x = request.session['x']
        print(email)
        user = User.objects.get(email=email)
        print(x)
        try:
            det = Dataform.objects.get(email=email)
            return render(request, 'roommate/dashboard.html', context={'detail': det.Verified, 'x': x, 'User': user, 'a': a})
        except Exception as e:
            a = True
        return render(request, 'roommate/dashboard.html', context={'x': x, 'User': user, 'a': a})
    except:
        return redirect(signup)



def coming_soon(request):
    return render(request,"Website/coming_soon.html")