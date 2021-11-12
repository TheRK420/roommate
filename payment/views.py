
from django.core.mail.message import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render,redirect
from dashboard.models import *

from django.views.decorators.csrf import csrf_exempt
import random
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from django.contrib.sites.shortcuts import get_current_site
MERCHANT_KEY = 'mN4Pw3JQOjbnPpy#'
from . import Checksum
from roomate.models import Dataform
from student.models import User as US

def Pay1(request):
    bookout=bookingrooms.objects.get(email=request.session['pay_email'],gender=request.session['gender'],hostel_name=request.session['hostel_name'],category=request.session['category'])
    id_new="_"+bookout.booking_id[1:]
    current_site = get_current_site(request)
    param_dict = {
        'MID': 'KxrEXO11204068668807',
        'ORDER_ID': str(id_new),
        'TXN_AMOUNT': str(int(bookout.total)-999),
        'CUST_ID': bookout.email,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        
        'CALLBACK_URL':'http://'+str(current_site)+'/handlerequest1/',
        }
    
    generated=Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    param_dict['CHECKSUMHASH'] = generated
    return render(request, 'Website/paytm.html', {'param_dict': param_dict})

@csrf_exempt
def handlerequest1(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    print(response_dict)
    success=False
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    id="#"+(str(response_dict['ORDERID'])[1:])
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            room=bookingrooms.objects.get(booking_id="#"+(str(response_dict['ORDERID'])[1:]))
            room.payment=True
            room.save()
            pl=payment_link.objects.get(orderid="#"+(str(response_dict['ORDERID'])[1:]))
            pl.transaction_id_full=response_dict['TXNID']
            pl.payment_modefull=response_dict['PAYMENTMODE']
            pl.transaction_datefull=response_dict['TXNDATE']
            pl.bank_transaction_idfull=response_dict['BANKTXNID']
            pl.bank_namefull=response_dict['BANKNAME']
            pl.save()
            send_mailtoVendor_Full(request,room.booking_id)
            send_mailtoStudent_Full(request,room.booking_id)
            success=True
        else:
            change_id=""
            pl=payment_link.objects.get(orderid="#"+(str(response_dict['ORDERID'])[1:]))
            room=bookingrooms.objects.get(booking_id="#"+(str(response_dict['ORDERID'])[1:]))
            pl_dummy=pl
            room_dummy=room
            pl.delete()
            room.delete()
            
            while True:
                change_id= "#"+str(random.randint(1000000,9000000))  
                try:
                    bookingrooms.objects.get(booking_id="#"+(str(response_dict['ORDERID'])[1:]))
                    continue
                except:
                    break
            bookingrooms(timestamp=room_dummy.timestamp,booking_id=change_id,logged_mail=room_dummy.logged_mail,cust_name=room_dummy.cust_name,category=room_dummy.category,hostel_name=room_dummy.hostel_name,gender=room_dummy.gender,email=room_dummy.email,contact=room_dummy.contact,college=room_dummy.college,branch=room_dummy.branch,date=room_dummy.date,city=room_dummy.city,year=room_dummy.year,duration=room_dummy.duration,total=room_dummy.total,confirmation=room_dummy.confirmation,payment=room_dummy.payment,reg_payment=room_dummy.reg_payment,rejected=room_dummy.rejected).save()
            payment_link(cust_name=pl_dummy.cust_name,email=pl_dummy.email,logged_mail=pl_dummy.logged_mail,hostel_name=pl_dummy.hostel_name,category=pl_dummy.category,amount=pl_dummy.amount,gender=pl_dummy.gender,orderid=change_id,transaction_id999=pl_dummy.transaction_id999,transaction_id_full=pl_dummy.transaction_id_full,payment_mode999=pl_dummy.payment_mode999,payment_modefull=pl_dummy.payment_modefull,transaction_date999=pl_dummy.transaction_date999,transaction_datefull=pl_dummy.transaction_datefull,bank_transaction_id999=pl_dummy.bank_transaction_id999,bank_transaction_idfull=pl_dummy.bank_transaction_idfull,bank_name999=pl_dummy.bank_name999,bank_namefull=pl_dummy.bank_namefull).save()
            prev_id="#"+(str(response_dict['ORDERID'])[1:])
            orderIdChangeMail(request,change_id,prev_id)
            print('order was not successful because' + response_dict['RESPMSG'])

    return render(request, 'payment/success.html', {'response': response_dict,'success':success,'id':id})


def orderIdChangeMail(request,change_id,prev_id):
    email_subject = 'Booking Id Change'
    # email=request.session['pay_email']    
    br=bookingrooms.objects.get(booking_id=change_id)
    ys=br
    v_email=Dataform.objects.get(hostel_name=br.hostel_name).email
    room=addroom.objects.get(category=br.category,hostel_name=br.hostel_name,email=v_email,gender=br.gender)
    name=br.cust_name
    html_message = render_to_string('payment/OrderIdChange.html',
                                    {
                                        'name':name,
                                        'room':room,
                                        'change_id':change_id,
                                        'prev_id':prev_id
                                    })
    email_body = strip_tags(html_message)
    
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [br.email])
    msg.attach_alternative(html_message, "text/html")
    msg.send()




 
def send_mailtoVendor_Full(request,id):
    email_subject = 'ROOM BOOKED'
    br=bookingrooms.objects.get(booking_id=id)
    data=Dataform.objects.get(hostel_name=br.hostel_name)
    room=addroom.objects.get(category=br.category,hostel_name=br.hostel_name,email=data.email,gender=br.gender)
    user=US.objects.get(email=br.logged_mail)
    amount=int(br.total)-999
    
    html_message = render_to_string('payment/VendorBooking_Complete.html',
                                    {
                                        'user':user,
                                        'name':data.Name,
                                        'room':room,
                                        'amount':amount
                                    }
                                    )
    email_body = strip_tags(html_message)
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [room.email])
    msg.attach_alternative(html_message, "text/html")
    msg.send()


def send_mailtoStudent_Full(request,id):
    email_subject = 'PAYMENT SUCCESSFULL'
    # email=request.session['pay_email']    
    br=bookingrooms.objects.get(booking_id=id)
    ys=br
    v_email=Dataform.objects.get(hostel_name=br.hostel_name).email
    room=addroom.objects.get(category=br.category,hostel_name=br.hostel_name,email=v_email,gender=br.gender)
    amount=int(ys.total)-999
    name=br.cust_name
    
    html_message = render_to_string('payment/StudentBooking_Complete.html',
                                    {
                                        'room':room,
                                        'name':name,
                                        'amount':amount,
                                        'book':br
                                    })
    email_body = strip_tags(html_message)
    
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [br.email])
    msg.attach_alternative(html_message, "text/html")
    msg.send()






@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    print(response_dict)
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    success=False
    id="#"+str(response_dict['ORDERID'])
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')

            room=bookingrooms.objects.get(booking_id="#"+str(response_dict['ORDERID']))
            room.reg_payment=True
            room.save()
            
            pl=payment_link.objects.get(orderid="#"+(str(response_dict['ORDERID'])))
            pl.transaction_id999=response_dict['TXNID']
            pl.payment_mode999=response_dict['PAYMENTMODE']
            pl.transaction_date999=response_dict['TXNDATE']
            pl.bank_transaction_id999=response_dict['BANKTXNID']
            pl.bank_name999=response_dict['BANKNAME']
            pl.save()
            send_mailtoVendor_999(request,room.booking_id)
            send_mailtoStudent_999(request,room.booking_id)
            success=True
        else:
            print("yaha per order cancel")
            room=bookingrooms.objects.get(booking_id="#"+str(response_dict['ORDERID']))
            room.delete()
            pl=payment_link.objects.get(orderid="#"+str(response_dict['ORDERID']))
            pl.delete()
            print('order was not successful because' + response_dict['RESPMSG'])



    return render(request, 'payment/success.html', {'response': response_dict,'success':success,'id':id})


def send_mailtoVendor_999(request,id):
    email_subject = 'NEW BOOKINGS'
    br=bookingrooms.objects.get(booking_id=id)
    
    room=addroom.objects.filter(hostel_name=br.hostel_name,category=br.category,gender=br.gender)[0]
    name=Dataform.objects.get(email=room.email).Name
    
    user=US.objects.get(email=br.logged_mail)
    amount_due= int(br.total)-999
    
    print("room is changed from ",room.num_room)
    room.num_room= str(int(room.num_room)-1)
    if(int(room.num_room)==0):
        sendmail_roomend(request,id)
        room.delete()
        
    print("to ",room.num_room)
    room.save()
    
    
    html_message = render_to_string('payment/Vendor_booking999.html',
                                    {
                                        'user':user,
                                        'name':name,
                                        'room':room,
                                        'amount_due':amount_due
                                    }
                                    )
    email_body = strip_tags(html_message)
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [room.email])
    msg.attach_alternative(html_message, "text/html")
    msg.send()



def send_mailtoStudent_999(request,id):
    email_subject = 'ROOMMATE PAYMENT Rs.999 COMPLETED'
    br=bookingrooms.objects.get(booking_id=id)
    email=br.email
    
    amount_due= int(br.total)-999
    print(amount_due)
    
    html_message = render_to_string('payment/Student_booking999.html',
                                    {
                                        'room':br,
                                        'amount_due':amount_due
                                    })
    email_body = strip_tags(html_message)
    
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [email])
    msg.attach_alternative(html_message, "text/html")
    
    msg.send()
    


def sendmail_roomend(request,id):
    email_subject = 'NO ROOMS REMAINING'
    br=bookingrooms.objects.get(booking_id=id)
    
    room=addroom.objects.filter(hostel_name=br.hostel_name,category=br.category,gender=br.gender)[0]
    name=Dataform.objects.get(email=room.email).Name
    html_message = render_to_string('payment/Vendor_RoomEnd.html',
                                    {
                                        'name':name,
                                        'room':room,
                                    }
                                    )
    email_body = strip_tags(html_message)
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_FROM_USER, [room.email])
    msg.attach_alternative(html_message, "text/html")
    msg.send()
