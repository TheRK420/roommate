
from django.core.mail.message import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render,redirect
#from dashboard.models import Order
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


def vendor_profile(request):
    email=request.session['email']
    vendor=Dataform.objects.get(email=email)
    return render(request,"dashboard/profile.html",context={'vendor':vendor})

def edit(request):
    email=request.session['email']
    vendor=Dataform.objects.get(email=email)
    print('karthik')
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
        print('1')
        print(useremail)
        user = User.objects.get(email=useremail)
        print('2')
        dp=Dataform.objects.get(email=useremail).Photo
        # print(user)
        print(user)
        print('3')
        return render(request, 'dashboard/index.html', {'user': user,'dp':dp})
    except User.DoesNotExist:
        return render(request, "dashboard/auth-login-v2.html", {"status": "Please login again"})


def added_room(request):
    email = request.session['email']
    print(email)
    rooms = addroom.objects.filter(email=email)
    print(rooms)
    i = 0
    #Paginator added
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
    print(email)
    if request.method == 'POST':
        print("Karthik")
        print(request.POST)
        # try:
        Df=Dataform.objects.get(email=email)
        name=Df.hostel_name
        discount = request.POST['discount']
        # category = request.POST['category']
        sharing=request.POST['sharing']
        sharing_cat=request.POST['AC']
        gender=request.POST['Gender']
        month=request.POST['months']
        price = request.POST['price']
        print("sharing",sharing)
        print("sharing_cat",sharing_cat)
        print("gender",gender)
        category=sharing+" "+sharing_cat
        # print(category)
        num_room = request.POST['num_room']
        # des = request.POST['description']    # to do this
        des=request.POST['more']  # sample
        print("request.FILES ", request.FILES)
        # print('1')
        img1 = request.FILES.get('pic1')
        img2 = request.FILES.get('pic2')
        img3 = request.FILES.get('pic3')
        img4 = request.FILES.get('pic4')
        img5 = request.FILES.get('pic5')
        img6 = request.FILES.get('pic6')
        date = datetime.date.today()
        # print('2')
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
        # print('3')
        # print(email,price,discount,category,num_room,date,Res,CrBs,St,BR,WF)d
        price=int(price)-(int(price)*int(discount)//100)
        print(price)
        
        
        
        
        
        addroom(description=des,email=email,category=category,month=month,hostel_name=name,num_room=num_room,discount=discount,gender=gender,price=price,image1=img1,image2=img2,image3=img3,image4=img4,image5=img5,image6=img6,date=date,Restaurant=Res,CarBus=CrBs,Stationary=St,BikeRent=BR,Wifi=WF,Laundry=Lan,Gym=Gym,Water=Water,CCTV=CCTV,verified=False).save()
        

        return redirect('added_room')
        # except:
        #     print("HI not done ")
        #     return redirect('add_room')
    print("get requeset")
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
        
    print(l)
    
    for i in book:
        if i.hostel_name in l:
            room.append(i)
    print(room)
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
    print(name)
    book=bookingrooms.objects.filter(hostel_name=name)
    for i in book:
        if i.confirmation==0 and i.rejected==0 and i.reg_payment==1:
            room.append((i))
            
            
    print(room)
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
    print(name)
    book=bookingrooms.objects.filter(hostel_name=name).order_by("-timestamp")
    for i in book:
        if i.confirmation==1 and i.payment==1:
            room.append(i)
    print(room)
    
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
    print(name)
    book=bookingrooms.objects.filter(hostel_name=name)
    for i in book:
        if i.confirmation==1 and i.rejected==0 and i.reg_payment==1 and i.payment==0:
            room.append(i)
    print(room)
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
    print(name)
    book=bookingrooms.objects.filter(hostel_name=name)
    for i in book:
        if i.rejected==1:
            room.append(i)
    print(room)
    P=Paginator(room,10)
    page=request.GET.get('page')
    pagi_rooms=P.get_page(page)
    return render(request, 'dashboard/rejected.html',context={'room':room,'pagi_rooms':pagi_rooms,'dp':dp,'user':user})


def confirm_booking(request,booking_id,hash,cat,gender):
    print(hash,cat,'BYE')
    hash=hash.replace("%20"," ")
    booking_id=booking_id.replace("%23","#")
    cat=cat.replace("%20"," ")
    gender=gender.replace("%20"," ")
    room=bookingrooms.objects.filter(booking_id=booking_id)

    email=room[0].email

    for i in room:
        i.confirmation=True
        i.save()
    # send_mail(request,email)
    send_activation_email(room,request)
    # return HttpResponse("done")
    # room=room[0]
    # current_site = get_current_site(request)
    # email_subject = 'Complete Payment Link Roomate'
    # html_message = render_to_string('dashboard/RemaingAmountMail.html', {
    #     'user': room.cust_name,
    #     'domain': current_site,
    #     'uid': room.email,
    #     'amount':int(room.total)-999,
    #     'category':room.category,
    #     'hostel_name':room.hostel_name,
    #     'token': generate_token.make_token(room)
    # })
    # payment_link(cust_name=room.cust_name,email=room.email,hostel_name=room.hostel_name,category=room.category,amount=int(room.total)-999,token= generate_token.make_token(room),gender=room.gender).save()
    # http://127.0.0.1:8000/payment-user/joshishivansh28012001@gmail.com/94001/Single%20Sharing/Aashiyana%20Grand/av6tv9-651b37bb9d023e928aa238004c3732a9
    # link="http://{{domain}}{% url 'payment_final' uidb64=uid amount=amount category=category hostel_name=hostel_name token=token %}"
    # return render(request,"dashboard/payment_Link.html",context={
    #     'user': room.cust_name,
    #     'domain': current_site,
    #     'uid': room.email,
    #     'amount':int(room.total)-999,
    #     'category':room.category,
    #     'hostel_name':room.hostel_name,
    #     'token': generate_token.make_token(room)
    # })
    return redirect(pendingorder)




# def send_mail(request,email):
#     email_subject = 'BOOKING REJECTED'
#     email_body = '''Respected sir/ma'am,

#     Your booking has been Rejected by the owner.
#     Your amount of RS.999 will be refunded within 24hrs. 

#     Regards, 
#     techmihirnaik group.'''
#     # html_message = render_to_string('roommate/single-news.html')
#     # email_body = strip_tags(html_message)
#     email = EmailMessage(subject=email_subject, body=email_body,
#                          from_email=settings.EMAIL_FROM_USER,
#                          to=[email]
#                          )
#     # msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [email])
#     # msg.attach_alternative(html_message, "text/html")
#     # print('HIII')
#     email.send()



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
    # for i in room:
    #     i.rejected=True
    #     i.save()
    hostel_name=room.hostel_name
    send_rejection(request,email,hostel_name,cat,gender)
    return redirect(neworder)





# changes done here , that is  removed thee hard code thing 
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
    
    # for i in ys:
    #     if(not i.rejected):
    html_message = render_to_string('dashboard/StudentBooking_Rejected.html',
                            {
                                'room':room,
                                # 'amount':amount,
                                'book':ys
                            })
    email_body = strip_tags(html_message)
    # email = EmailMessage(subject=email_subject, body=email_body,
    #                      from_email=settings.EMAIL_FROM_USER,
    #                      to=[email]
    #                      )
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [email])
    msg.attach_alternative(html_message, "text/html")
    # print('HIII')
    msg.send()
            # continue
            
    # user=User.objects.get(email=ys.logged_mail)
    # amount=int(room.price)
    # print("shivahs")
    # print(user.student_id)
#     email_body = '''Respected sir/ma'am,

#    Your payment of Rs.999 has been recieved.
#    Wait for the confirmation from the Owner


#     Regards, 
#     techmihirnaik group.'''
    






def send_activation_email(room, request):
    room=room[0]
    
    current_site = get_current_site(request)
    email_subject = 'Complete Payment Link on Dashboard'
    amount=int(room.total)-999
    html_message = render_to_string('dashboard/RemaingAmountMail.html',{'amount':amount})
    email_body = strip_tags(html_message)
    # email = EmailMessage(subject=email_subject, body=email_body,
    #                      from_email=settings.EMAIL_FROM_USER,
    #                      to=[room.email]
    #                      )
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [room.email])
    msg.attach_alternative(html_message, "text/html")
    # print('HIII')
    msg.send()
    # payment_link(cust_name=room.cust_name,email=room.email,hostel_name=room.hostel_name,category=room.category,amount=int(room.total)-999,token= generate_token.make_token(room),gender=room.gender).save()
    
    payment_link(cust_name=room.cust_name,email=room.email,hostel_name=room.hostel_name,category=room.category,amount=int(room.total)-999,token= generate_token.make_token(room),gender=room.gender).save()
    # return render(request,"dashboard/payment_Link.html",context={
    #     'user': room.cust_name,
    #     'domain': current_site,
    #     'uid': room.email,
    #     'amount':int(room.total)-999,
    #     'category':room.category,
    #     'hostel_name':room.hostel_name,
    #     'token': generate_token.make_token(room)
    # })





def activate_user(request,uidb64,amount,category,hostel_name,gender,token):
    # uidb64 is email
    hostel_name=hostel_name.replace("%20"," ")
    category=category.replace("%20"," ")
    gender=gender.replace("%20"," ")
    # user= bookingrooms.objects.get(email=uidb64)
    # print(user)
    # user.payment = True
    # user.save()
    request.session['status']='Payment Successfull!!'
    request.session['pay_email']=uidb64
    request.session['amount']=int(amount)*100
    request.session['category']=category
    request.session['gender']=gender
    request.session['hostel_name']=hostel_name
    return redirect(payment_before1)


def payment_before1(request):
    # email=request.session['email']
    # n=request.session['n']
    # print(request.POST,request.GET)
    # user=User.objects.get(email=email)
    
    # amount = 50000
    cat=request.session['category']
    hn=request.session['hostel_name']
    email=request.session['pay_email']
    print(bookingrooms.objects.all())
    user= bookingrooms.objects.get(email=email,category=cat,hostel_name=hn,gender=request.session['gender'],rejected=False,confirmation=True)
    
    amount=request.session['amount']
    
    # customer= request.POST['dzName']
    # print("Karthik")
    # print(request.POST)
    # print(customer)
    client = razorpay.Client(auth=("rzp_test_MwnCyVMp8jNqyp", "SUcxn8l0OfRoR1eRDGGHKQcR"))
    payment = client.order.create({'amount': amount, 'currency': 'INR','payment_capture': '1'})
    
    return render(request, 'dashboard/pay.html',context={'n':user.cust_name,'test_email':user.email,'contact':user.contact,'amount':amount,'normal_amount':int(amount)//100})



@csrf_exempt
def payment_after1(request):
    cat=request.session['category']
    hn=request.session['hostel_name']
    email=request.session['pay_email']
    user= bookingrooms.objects.get(email=email,category=cat,hostel_name=hn,gender=request.session['gender'],rejected=False,confirmation=True)
    
    user.payment=True
    user.save()
    
    send_mail(request)
    send_mailtoVendor(request)
    return redirect(show_bookings)





# changes done here , that is  removed thee hard code thing 
def send_mailtoVendor(request):
    email_subject = 'ROOM BOOKED'
    # email=request.session['email']

    data=Dataform.objects.get(hostel_name=request.session['hostel_name'])
    ys=bookingrooms.objects.get(email=request.session['pay_email'],category=request.session['category'],hostel_name=request.session['hostel_name'],rejected=False,gender=request.session['gender'])
    room=addroom.objects.get(category=request.session['category'],hostel_name=request.session['hostel_name'],email=data.email,gender=ys.gender)
    user=US.objects.get(email=ys.logged_mail)
    # amount=int(room.price)
    amount=int(ys.total)-999
    print("shivahs")
    print(user.student_id)
    
    
    
    
    html_message = render_to_string('dashboard/VendorBooking_Complete.html',
                                    {
                                        'user':user,
                                        'name':data.Name,
                                        'room':room,
                                        'amount':amount
                                    }
                                    )
    email_body = strip_tags(html_message)
    # email = EmailMessage(subject=email_subject, body=email_body,
    #                      from_email=settings.EMAIL_FROM_USER,
    #                      to=[email]
    #                      )
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [room.email])
    msg.attach_alternative(html_message, "text/html")
    # print('HIII')
    msg.send()









# changes done here , that is  removed thee hard code thing 
def send_mail(request):
    email_subject = 'PAYMENT SUCCESSFULL'
    email=request.session['pay_email']    
    
    ys=bookingrooms.objects.get(email=request.session['pay_email'],category=request.session['category'],hostel_name=request.session['hostel_name'],rejected=False,gender=request.session['gender'])
    v_email=Dataform.objects.get(hostel_name=request.session['hostel_name']).email
    room=addroom.objects.get(category=request.session['category'],hostel_name=request.session['hostel_name'],email=v_email,gender=ys.gender)
    amount=int(ys.total)-999
    
    # user=User.objects.get(email=ys.logged_mail)
    # amount=int(room.price)
    # print("shivahs")
    # print(user.student_id)
#     email_body = '''Respected sir/ma'am,

#    Your payment of Rs.999 has been recieved.
#    Wait for the confirmation from the Owner


#     Regards, 
#     techmihirnaik group.'''
    html_message = render_to_string('dashboard/StudentBooking_Complete.html',
                                    {
                                        'room':room,
                                        'amount':amount,
                                        'book':ys
                                    })
    email_body = strip_tags(html_message)
    # email = EmailMessage(subject=email_subject, body=email_body,
    #                      from_email=settings.EMAIL_FROM_USER,
    #                      to=[email]
    #                      )
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [email])
    msg.attach_alternative(html_message, "text/html")
    # print('HIII')
    msg.send()









# # changes done here , that is  removed thee hard code thing 
# def send_mail(request):
#     email_subject = 'PAYMENT SUCCESSFULL'
#     email=request.session['pay_email']
#     email_body = '''Respected sir/ma'am,

#     Your Payment has been successfully done.
#     You'r allocated with your specified room.

#     Regards, 
#     techmihirnaik group.'''
#     # html_message = render_to_string('roommate/single-news.html')
#     # email_body = strip_tags(html_message)
#     email = EmailMessage(subject=email_subject, body=email_body,
#                          from_email=settings.EMAIL_FROM_USER,
#                          to=[email]
#                          )
#     # msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [email])
#     # msg.attach_alternative(html_message, "text/html")
#     # print('HIII')
#     email.send()
    
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

# def viewcomments(request,name,value,id):
#     c=comments.objects.get(student_name=name,id=id)
#     c.published=value
#     c.save()
#     return redirect(reviews)

# def unviewcomments(request,name,value,id):
#     c=comments.objects.get(student_name=name,id=id)
#     c.published=value
#     c.save()
#     return redirect(reviews)


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
    # print(request.session['cate'])
    # print(request.session['cust_email'])
    # hostel_name=Dataform.objects.get(email=request.session['email']).hostel_name
    print("hello")
    id=request.session['id']
    id=id.replace("%23","#")
    print("Id")
    print(id)
    room=bookingrooms.objects.get(booking_id=id)
    d=addroom.objects.get(gender=room.gender,hostel_name=room.hostel_name,category=room.category)
    # previous=int(100/(100-int(d.discount))*int(d.price))
    discount=int(d.discount)
    user=User.objects.get(email=request.session['email'])
    # dp=US.objects.get(email=request.session['email']).photo
    dp= Dataform.objects.get(email=request.session['email']).Photo
    return render(request,'dashboard/order-details.html',context={'room':room,'discount':discount,'previous':d.price,'user':user,'dp':dp})