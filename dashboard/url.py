from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings # new
from django.conf.urls.static import static # new

urlpatterns = [
    path('vendor_profile',views.vendor_profile,name='vendor_profile'),
    path("edit",views.edit,name='edit'),
    path('editing',views.editing,name='editing'),
    path('index.html',views.dashboard,name='dashboard'),
    path('added-room.html',views.added_room,name='added_room'),
    path('add-room.html',views.add_room,name='add_room'),
    path('all.html',views.allorders,name='all'),
    path('orders-new.html',views.neworder,name='neworder'),
    path('completed.html',views.completedorder,name='completed'),
    path('pending.html',views.pendingorder,name='pendings'),
    path('rejected.html',views.rejectedorder,name='rejected'),
    path('reviews',views.reviews,name='reviews'),
    path('order-details.html',views.order_details,name=''),
    path('confirm_booking/<booking_id>/<hash>/<cat>/<gender>', views.confirm_booking, name="confirm_booking"),
    path('Reject_booking/<booking_id>/<hash>/<cat>/<gender>', views.Reject_booking, name="Reject_booking"),
    path('payment-user/<uidb64>/<amount>/<category>/<hostel_name>/<gender>',views.activate_user, name='payment_final'),
    path('order-det/<id>',views.order_details,name='order_details_data'),
    path('order-details',views.order_details_show,name='order_details_show'),
]
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)