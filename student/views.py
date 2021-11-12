
from django.shortcuts import render
from django.core import serializers
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from student.models import User,Reviews,comments
from dashboard.models import *
from roomate.models import Dataform
# import datetime
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.core.paginator import Paginator
import random
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
MERCHANT_KEY = 'mN4Pw3JQOjbnPpy#'
from payment import Checksum
from payment.views import *
from student.models import User as US
from dateutil.relativedelta import relativedelta
    
def trans(request):
    return render(request,'Website/transactions.html')

def myprofile(request):
    email = request.session['email']
    print(email)
    try:
        user = User.objects.get(email=email)
        print(user.contact)
        return render(request, 'Website/profile.html', context={'email': email, 'user': user})
    except:
        return render(request, 'Website/MY-PROFILE.html', context={'email': email})


def add_profile(request):
    name = request.POST['name']
    photo = request.FILES.get('photo')
    aadhar = request.FILES.get('aadhar')
    contact = request.POST['contact']
    city = request.POST['city']
    address = request.POST['address']
    college = request.POST['college']
    branch = request.POST['branch']
    year = request.POST['year']
    email = request.session['email']
    while True:
        s_id= "tech_stu"+ str(random.randint(1000000,9000000))  
        try:
            User.objects.get(student_id=s_id)
            continue
        except:
            break
    user = User(student_id=s_id,Name=name, photo=photo, aadhar=aadhar, contact=contact,address=address,city=city,
                email=email, college=college, branch=branch, year=year)
    user.save()
    return redirect(myprofile)


def listing123(request):
    email=request.session['email']
    room=Dataform.objects.filter(Verified=True)
    
    P=Paginator(room,10)
    page=request.GET.get('page')
    pagi_rooms=P.get_page(page)

    return render(request,'Website/Listing.html',context={'room':room,'pagi_rooms':pagi_rooms})

def edit_profile(request):
    email=request.session['email']
    user=User.objects.get(email=email)
    return render(request,'Website/edit-details.html',context={'user':user})

def editing_profile(request):
    email=request.session['email']
    user=User.objects.get(email=email)
    user.Name=request.POST.get('name')
    user.contact=request.POST.get('contact')
    user.address=request.POST.get('address')
    user.city=request.POST.get('city')
    user.college=request.POST.get('college')
    user.branch=request.POST.get('branch')
    user.year=request.POST.get('year')
    photo=request.FILES.get('dp')
    if(photo!=None):
        user.photo=photo
    user.save()
    return redirect(myprofile)

# discuss this
def view_details(request,Category,email,gender):
    Category=Category.replace("%20"," ")
    email=email.replace("%20"," ")
    request.session['cat']=Category
    request.session['gen']=gender
    request.session['room_email']=email
    return redirect(listing)

def listing(request):
    print("Shivansh gender",request.session['gen'])
    if "error" in request.session.keys():
        del request.session["error"]
    x=request.session['cat']
    y=request.session['room_email']
    email=request.session['email']
    print("shivansh")
    print(x,'cat')
    print(y,'room_email')
    hostel=addroom.objects.get(category=x,email=y,gender=request.session['gen'])
    detail=[]
    previous=int(100/(100-int(hostel.discount))*int(hostel.price))
    gender=request.session['gen']
    print(hostel)
    print("shivanhs email- ",email)
    toReview=False
    try:
        Reviews.objects.get(email=email,hostel_name=request.session['ho'],category=x,gender=request.session['gen'])
    except:
        toReview=True
        
    count=0
    space=0
    quality=0
    location=0
    service=0
    price=0
    avg=0
    try:
        allReview=Reviews.objects.filter(hostel_name=request.session['ho'],category=x,gender=request.session['gen'])
        print(allReview)
        for i in allReview:
            count+=1
            quality+=int(i.Quality)
            location+=int(i.Location)
            space+=int(i.Space)
            service+=int(i.Service)
            price+=int(i.Price)
        space/=count
        print(space)
        space = float("{:.1f}".format(space))
        print(space)
        
        quality/=count
        quality = float("{:.1f}".format(quality))
        print(quality)
        
        location/=count
        location = float("{:.1f}".format(location))
        print(location)
    
        service/=count
        service = float("{:.1f}".format(service))
        print(service)
        price/=count
        price = float("{:.1f}".format(price))
        print(price)
        
        avg=(space+quality+location+service+price)/5
        avg = float("{:.1f}".format(avg))
        print(avg)
    except:
        pass
    c=comments.objects.filter(category=x,hostel_name=request.session['ho'],gender=request.session['gen'])
    return render(request,'Website/LISTING-DETAILS-3Signin.html',context={'c':c,'gender':gender,'room':hostel,'previous':previous,'count':count,'email':email,'cat':x,'avg':avg,'toReview':toReview,'space':space,'quality':quality,'location':location,'service':service,'price':price})





def add_review(request):
    if(request.method=="POST"):
        email=request.session['email']
        quality=request.POST.get('quality')
        location=request.POST.get('location')
        space=request.POST.get('space')
        service=request.POST.get('service')
        price=request.POST.get('price')
        Reviews(email=email,hostel_name=request.session['ho'],category=request.session['cat'],gender=request.session['gen'],Quality=quality,Location=location,Space=space,Service=service,Price=price).save()
    return redirect(listing)

def hostel_name(request,hostel):
    print("ranjeet",hostel)
    hostel=hostel.replace("%20"," ")
    request.session['ho']=hostel
    return redirect(rooms)

def rooms(request):
    try:
        hostel=request.session['ho']
        rooms=addroom.objects.filter(hostel_name=hostel, verified=True)

        email=request.session['email']
        User.objects.get(email=email)
        newroom=[]
        for i in rooms:
            previous=int(100/(100-int(i.discount))*int(i.price))
            if(int(i.num_room)>0):
                newroom.append((i,previous))
        return render(request,'Website/hostel-rooms.html',context={'hostel_name':hostel,'rooms':newroom})
    except:
        return redirect(myprofile)


import datetime

def booking(request):
    # try:
    date = datetime.date.today()
    name=request.POST['dzName']
    request.session['n']=name
    gender=request.POST['hostel_type']
    email=request.POST['email']
    contact=request.POST['contact']
    college=request.POST['college']
    branch=request.POST['branch']
    city=request.POST['city']
    year=request.POST['year']
    duration=request.POST['duration']
    confirmation=False
    rejected=False
    
    cat1=addroom.objects.get(category=request.session['cat'],hostel_name=request.session['ho'],gender=gender)
    cost=cat1.price
    per=cat1.month
    print("per = ",per)
    if(per=="1 month"):
        dur= int(duration[:2])
        cost=int(cost)*dur
    elif(per=="6 month"):
        if(duration=='12 month'):
            cost=int(cost)*2
    else:
        print("pass")
            
    hostel_name=cat1.hostel_name
    
    while True:
        booking_id= "#"+str(random.randint(1000000,9000000))  
        try:
            bookingrooms.objects.get(booking_id=booking_id)
            continue
        except:
            break
        
    b=bookingrooms.objects.filter(email=email,hostel_name=hostel_name,category=request.session['cat'],reg_payment=False,rejected=False,gender=gender,payment=False,confirmation=False)
    for i in b:
        i.delete()
    
    if(bookingrooms.objects.filter(email=email,hostel_name=hostel_name,category=request.session['cat'],reg_payment=True,rejected=False,gender=gender).exists()):
        
        a=bookingrooms.objects.get(email=email,hostel_name=hostel_name,category=request.session['cat'],reg_payment=True,rejected=False,gender=gender)
        if(datetime.date.today() > a.timestamp.date()+ relativedelta(months=+int(duration[0:2]))):
            a.delete()
            request.session['error']='Please try once again ! '
            return redirect(errorlisting)
        else:
            request.session['error']='This room is already booked by this mail id'
            return redirect(errorlisting)
    else:
        book=bookingrooms(booking_id=booking_id,cust_name=name,hostel_name=hostel_name,gender=gender,email=email,contact=contact,college=college,branch=branch,city=city,year=year,category=request.session['cat'],duration=duration,confirmation=confirmation,rejected=rejected,date=date,total=cost,logged_mail=request.session['email']).save()
        bookout=bookingrooms.objects.get(booking_id=booking_id)
        payment_link(cust_name=bookout.cust_name,email=bookout.email,hostel_name=bookout.hostel_name,category=bookout.category,amount=int(bookout.total)-999,gender=bookout.gender,logged_mail=bookout.logged_mail,orderid=bookout.booking_id).save()
        
        request.session['book_test_email']=email
        request.session['book_test_phone']=contact
        request.session['hostel_name']=hostel_name
        request.session['booking_category']=request.session['cat']
        id_new=bookout.booking_id[1:]
        current_site = get_current_site(request)
        param_dict = {
            'MID': 'KxrEXO11204068668807',
            'ORDER_ID': str(id_new),
            'TXN_AMOUNT': "999",
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://'+str(current_site)+'/handlerequest/',
            }
        
        generated=Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        
        param_dict['CHECKSUMHASH'] = generated
        
        return render(request, 'Website/paytm.html', {'param_dict': param_dict})
    # except:
    #     messages.error(request,'Data already taken')
    #     return redirect(booking)






def errorlisting(request):
    x=request.session['cat']
    y=request.session['room_email']
    email=request.session['email']
    error=request.session['error']
    hostel=addroom.objects.get(category=x,email=y,gender=request.session['gen'])
    previous=int(100/(100-int(hostel.discount))*int(hostel.price))
    gender=request.session['gen']
    toReview=False
    try:
        Reviews.objects.get(email=email,hostel_name=request.session['ho'],category=x,gender=request.session['gen'])
    except:
        toReview=True
        
    count=0
    space=0
    quality=0
    location=0
    service=0
    price=0
    avg=0
    try:
        allReview=Reviews.objects.filter(hostel_name=request.session['ho'],category=x,gender=request.session['gen'])
        print(allReview)
        for i in allReview:
            count+=1
            quality+=int(i.Quality)
            location+=int(i.Location)
            space+=int(i.Space)
            service+=int(i.Service)
            price+=int(i.Price)
        space/=count
        print(space)
        space = float("{:.1f}".format(space))
        print(space)
        
        quality/=count
        quality = float("{:.1f}".format(quality))
        print(quality)
        
        location/=count
        location = float("{:.1f}".format(location))
        print(location)
    
        service/=count
        service = float("{:.1f}".format(service))
        print(service)
        price/=count
        price = float("{:.1f}".format(price))
        print(price)
        
        avg=(space+quality+location+service+price)/5
        avg = float("{:.1f}".format(avg))
        print(avg)
    except:
        pass
    c=comments.objects.filter(category=x,hostel_name=request.session['ho'],gender=request.session['gen'])
    return render(request,'Website/LISTING-DETAILS-3Signin.html',context={'error':error,'c':c,'gender':gender,'room':hostel,'previous':previous,'count':count,'email':email,'cat':x,'avg':avg,'toReview':toReview,'space':space,'quality':quality,'location':location,'service':service,'price':price})


def payment_page(request):
    cat=request.session['cat']
    return HttpResponseRedirect('https://rzp.io/l/3UCI3Y0g0')


def show_bookings(request):
    email=request.session['email']
    x=request.session['x']
    rooms=bookingrooms.objects.filter(logged_mail=email).order_by('-timestamp')
    user=User.objects.get(email=email)
    name=user.Name
    dp=user.photo.url
    detail=[]
    
    
    for i in rooms:
        if i.reg_payment:
            i.total=int(i.total)-999
        if(i.confirmation and i.reg_payment):
            a=payment_link.objects.get(orderid=i.booking_id)
            detail.append((True,i,a))
        else:
            detail.append((False,i,None))
            
    return render(request,'Website/mybookings.html',context={'rooms':rooms,'name':name,'dp':dp,'detail':detail})



def order_details1(request,booking):
    request.session['detail']=booking
    return redirect(show_detail)


def show_detail(request):
    b=request.session['detail']
    b=b.replace("%23","#")
    a=bookingrooms.objects.get(booking_id=b)
    confirm=a.confirmation and a.reg_payment and a.payment
    reject=a.reg_payment and a.rejected 
    pending=a.reg_payment and (not a.rejected) and (not a.payment) and (not a.confirmation)
    
    d=addroom.objects.get(hostel_name=a.hostel_name,category=a.category,gender=a.gender)
    
    discount=int(d.discount)
    user=User.objects.get(email=request.session['email'])
    dp=US.objects.get(email=user.email).photo.url
    
    return render(request,'Website/order-details.html',context={"user":user,"detail":a,'reject':reject,'confirm':confirm,'pending':pending,'discount':discount,'previous':d.price,'dp':dp})



def comment(request):
    if request.method == 'POST':
        print("comonent out")
        print(request.POST)
        coment = request.POST['comments']
        category = request.session['cat']
        vendor_email = request.session['room_email']
        email = request.session['email']
        user = User.objects.get(email=email)       
        date = datetime.date.today()
        gender= request.session['gen']
        comments(comment=coment, category=category, date_comment=date,gender=gender,email_vendor=vendor_email, student_name=user.Name,hostel_name=request.session['ho']).save()
    return redirect(listing)

