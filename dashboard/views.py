
from django.core.mail.message import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.core import serializers
from roomate.models import Dataform,User
from dashboard.models import *
from student.models import User as US
import datetime
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError

from roomate.views import register
from student.views import booking, hostel_name, show_bookings
from .utils import generate_token

from django.core.mail import EmailMessage
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
import random
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from student.models import comments
from payment.url import *
from payment.views import *



def vendor_profile(request):
    email=request.session['email']
    vendor=Dataform.objects.get(email=email)
    return render(request,"dashboard/profile.html",context={'vendor':vendor})

def edit(request):
    email=request.session['email']
    vendor=Dataform.objects.get(email=email)
    return render(request,'dashboard/edit-details.html',context={'vendor':vendor})

def editing(request):
    email=request.session['email']
    vendor=Dataform.objects.get(email=email)
    vendor.Name=request.POST.get('name')
    vendor.hcontact=request.POST.get('phone')
    vendor.hostel_name=request.POST.get('hostel_name')
    vendor.address=request.POST.get('address')
    Photo=request.FILES.get('photo')
    if(Photo!=None):
        vendor.Photo=Photo
    vendor.save()
    return redirect(vendor_profile)

def dashboard(request):
    useremail = request.session['email']
    try:
        user = User.objects.get(email=useremail)
        dp=Dataform.objects.get(email=useremail).Photo
        print(user)
        return render(request, 'dashboard/index.html', {'user': user,'dp':dp})
    except User.DoesNotExist:
        return render(request, "dashboard/auth-login-v2.html", {"status": "Please login again"})


def added_room(request):
    email = request.session['email']
    rooms = addroom.objects.filter(email=email)
    i = 0
    P=Paginator(rooms,10)
    page=request.GET.get('page')
    pagi_rooms=P.get_page(page)
    dp=Dataform.objects.get(email=email).Photo
    user=User.objects.get(email=email)
    return render(request, 'dashboard/added-room.html', context={'room': rooms, 'i': i,'pagi_rooms':pagi_rooms,'dp':dp,'user':user})



def add_room(request):
    email = request.session['email']
    dp=Dataform.objects.get(email=email).Photo
    user= User.objects.get(email=email)
    if request.method == 'POST':
        Df=Dataform.objects.get(email=email)
        name=Df.hostel_name
        discount = request.POST['discount']
        sharing=request.POST['sharing']
        sharing_cat=request.POST['AC']
        gender=request.POST['Gender']
        month=request.POST['months']
        price = request.POST['price']
        category=sharing+" "+sharing_cat
        num_room = request.POST['num_room']
        des=request.POST['more'] 
        img1 = request.FILES.get('pic1')
        img2 = request.FILES.get('pic2')
        img3 = request.FILES.get('pic3')
        img4 = request.FILES.get('pic4')
        img5 = request.FILES.get('pic5')
        img6 = request.FILES.get('pic6')
        date = datetime.date.today()
        Res=False;CrBs=False;St=False;BR=False;WF=False;Lan=False;Gym=False;Water=False;CCTV=False;
        try:
            request.POST['Restaurant']
            Res=True
        except:
            pass
        try:
            request.POST['Car/Bus']
            CrBs=True
        except:
            pass
        try:
            request.POST['Stationary']
            St=True
        except:
            pass
        try:
            request.POST['Bike Rentals']
            BR=True
        except:
            pass
        try:
            request.POST['Wifi']
            WF=True
        except:
            pass
        try:
            request.POST['Laundry']
            Lan=True
        except:
            pass
        try:
            request.POST['Gym']
            Gym=True
        except:
            pass
        try:
            request.POST['Water']
            Water=True
        except:
            pass
        try:
            request.POST['Cctv']
            CCTV=True
        except:
            pass
        price=int(price)-(int(price)*int(discount)//100)
        addroom(description=des,email=email,category=category,month=month,hostel_name=name,num_room=num_room,discount=discount,gender=gender,price=price,image1=img1,image2=img2,image3=img3,image4=img4,image5=img5,image6=img6,date=date,Restaurant=Res,CarBus=CrBs,Stationary=St,BikeRent=BR,Wifi=WF,Laundry=Lan,Gym=Gym,Water=Water,CCTV=CCTV,verified=False).save()
        return redirect('added_room')
    
    d=Dataform.objects.get(email=request.session['email'])
    ans=1 
    if(d.category=="Male"):
        ans=2
    elif(d.category=="Female"):
        ans=3
    male=False
    female=False
    unisex=False
    if(ans==1):
        unisex=True
    elif(ans==2):
        male=True
    else:
        female=True
    return render(request, 'dashboard/add-room.html',{"user":user,"dp":dp,"ans":ans,"unisex":unisex,"male":male,"female":female})   # GET request

def order_details(request):
    return render(request,'dashboard/order-details.html')

def order_invoice(request):
    return render(request,'dashboard/order-invoice.html')


def allorders(request):
    email=request.session['email']
    l=[]
    room=[]
    book=bookingrooms.objects.all()
    rooms=addroom.objects.filter(email=email)
    for k in rooms:
        l.append(k.hostel_name)
        
    
    for i in book:
        if i.hostel_name in l:
            room.append(i)
    P=Paginator(book,10)
    page=request.GET.get('page')
    pagi_rooms=P.get_page(page)
    user=User.objects.get(email=email)
    dp=Dataform.objects.get(email=email).Photo
    return render(request, 'dashboard/all.html',context={'room':room,'pagi_rooms':pagi_rooms,'user':user,'dp':dp})


def neworder(request):
    email=request.session['email']
    dp=Dataform.objects.get(email=email).Photo
    user = User.objects.get(email=email)
    room=[]
    hostel=Dataform.objects.get(email=email)
    name=hostel.hostel_name
    book=bookingrooms.objects.filter(hostel_name=name)
    for i in book:
        if i.confirmation==0 and i.rejected==0 and i.reg_payment==1:
            room.append((i))
            
            
    P=Paginator(room,10)
    page=request.GET.get('page')
    pagi_rooms=P.get_page(page)
    
    
    return render(request, 'dashboard/orders-new.html',context={'room':room,'pagi_rooms':pagi_rooms,'dp':dp,'user':user})


def completedorder(request):
    email=request.session['email']
    dp=Dataform.objects.get(email=email).Photo
    user = User.objects.get(email=email)
    room=[]
    hostel=Dataform.objects.get(email=email)
    name=hostel.hostel_name
    book=bookingrooms.objects.filter(hostel_name=name).order_by("-timestamp")
    for i in book:
        if i.confirmation==1 and i.payment==1:
            room.append(i)
    
    P=Paginator(room,10)
    page=request.GET.get('page')
    pagi_rooms=P.get_page(page)
    
    return render(request, 'dashboard/completed.html',context={'room':room,'pagi_rooms':pagi_rooms,'dp':dp,'user':user})


def pendingorder(request):
    email=request.session['email']
    dp=Dataform.objects.get(email=email).Photo
    user = User.objects.get(email=email)
    room=[]
    hostel=Dataform.objects.get(email=email)
    name=hostel.hostel_name
    book=bookingrooms.objects.filter(hostel_name=name)
    for i in book:
        if i.confirmation==1 and i.rejected==0 and i.reg_payment==1 and i.payment==0:
            room.append(i)
    P=Paginator(room,10)
    page=request.GET.get('page')
    pagi_rooms=P.get_page(page)
    
    return render(request, 'dashboard/pending.html',context={'room':room,'pagi_rooms':pagi_rooms,'dp':dp,'user':user})


def rejectedorder(request):
    email=request.session['email']
    dp=Dataform.objects.get(email=email).Photo
    user = User.objects.get(email=email)
    room=[]
    hostel=Dataform.objects.get(email=email)
    name=hostel.hostel_name
    book=bookingrooms.objects.filter(hostel_name=name)
    for i in book:
        if i.rejected==1:
            room.append(i)
    P=Paginator(room,10)
    page=request.GET.get('page')
    pagi_rooms=P.get_page(page)
    return render(request, 'dashboard/rejected.html',context={'room':room,'pagi_rooms':pagi_rooms,'dp':dp,'user':user})


def confirm_booking(request,booking_id,hash,cat,gender):
    hash=hash.replace("%20"," ")
    booking_id=booking_id.replace("%23","#")
    cat=cat.replace("%20"," ")
    gender=gender.replace("%20"," ")
    room=bookingrooms.objects.filter(booking_id=booking_id)

    email=room[0].email

    for i in room:
        i.confirmation=True
        i.save()
    send_activation_email(room,request)
    return redirect(pendingorder)




def Reject_booking(request,booking_id,hash,cat,gender):
    print(hash,cat,'HI')
    hash=hash.replace("%20"," ")
    booking_id=booking_id.replace("%20"," ")
    cat=cat.replace("%20"," ")
    gender=gender.replace("%20"," ")
    room=bookingrooms.objects.get(booking_id=booking_id,cust_name=hash,category=cat,rejected=False,gender=gender)
    print(room)
    email=room.email
    room.rejected=True
    room.save()
    hostel_name=room.hostel_name
    send_rejection(request,email,hostel_name,cat,gender)
    return redirect(neworder)



def send_rejection(request,email,hostel_name,cat,gender):
    print("karthik")
    print(email,hostel_name,cat)
    email_subject = 'BOOKING REJECTED'
    room=addroom.objects.get(category=cat,hostel_name=hostel_name,email=request.session['email'],gender=gender)
    room.num_room= str(int(room.num_room)+1)
    room.save()

    ys=bookingrooms.objects.filter(email=email,category=cat,hostel_name=hostel_name,rejected=True,gender=gender)
    
    
    res=None
    for i in ys:
        res=i
        
    ys=res
    pl=payment_link.objects.get(orderid=ys.booking_id)
    pl.delete()
    html_message = render_to_string('dashboard/StudentBooking_Rejected.html',
                            {
                                'room':room,
                                'book':ys
                            })
    email_body = strip_tags(html_message)
    # email = EmailMessage(subject=email_subject, body=email_body,
    #                      from_email=settings.EMAIL_FROM_USER,
    #                      to=[email]
    #                      )
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [email])
    msg.attach_alternative(html_message, "text/html")
    msg.send()



def send_activation_email(room, request):
    room=room[0]
    
    current_site = get_current_site(request)
    email_subject = 'Complete Payment Link on Dashboard'
    amount=int(room.total)-999
    html_message = render_to_string('dashboard/RemaingAmountMail.html',{'amount':amount})
    email_body = strip_tags(html_message)
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [room.email])
    msg.attach_alternative(html_message, "text/html")
    msg.send()
    




def activate_user(request,uidb64,amount,category,hostel_name,gender):
    hostel_name=hostel_name.replace("%20"," ")
    category=category.replace("%20"," ")
    gender=gender.replace("%20"," ")
    request.session['status']='Payment Successfull!!'
    request.session['pay_email']=uidb64
    request.session['amount']=int(amount)*100
    request.session['category']=category
    request.session['gender']=gender
    request.session['hostel_name']=hostel_name
    return redirect(Pay1)



    
def reviews(request):
    email=request.session['email']
    print(email)
    data=comments.objects.filter(email_vendor=email)
    print(data)
    print("karthik")
    
    P=Paginator(data,10)
    page=request.GET.get('page')
    pagi_rooms=P.get_page(page)
    print(data)
    user=User.objects.get(email=email)
    dp=Dataform.objects.get(email=email).Photo
    
    return render(request, 'dashboard/reviews.html',context={'c':data,'pagi_rooms':pagi_rooms,'user':user,'dp':dp})


def calender(request):
    return render(request, 'dashboard/calendar.html')


def chat(request):
    return render(request, 'dashboard/chat.html')


def todo(request):
    return render(request, 'dashboard/todo.html')



def order_details(request,id):
    request.session['id']=id
    print(request.session['id'])
    return redirect(order_details_show)

def order_details_show(request):
    print("hello")
    id=request.session['id']
    id=id.replace("%23","#")
    print("Id")
    print(id)
    room=bookingrooms.objects.get(booking_id=id)
    d=addroom.objects.get(gender=room.gender,hostel_name=room.hostel_name,category=room.category)
    discount=int(d.discount)
    user=User.objects.get(email=request.session['email'])
    dp= Dataform.objects.get(email=request.session['email']).Photo
    return render(request,'dashboard/order-details.html',context={'room':room,'discount':discount,'previous':d.price,'user':user,'dp':dp})