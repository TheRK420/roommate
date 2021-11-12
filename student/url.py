from django.contrib.auth import login
from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings # new
from django.conf.urls.static import static # new
from django.views.generic import TemplateView

urlpatterns = [
    path('myprofile',views.myprofile,name='myprofile'),
    path('add_profile',views.add_profile,name='add_profile'),
    path('listings',views.listing123,name='listing'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('editing_profile',views.editing_profile,name='editing_details'),
    path('details/<Category>/<email>/<gender>',views.view_details,name='details'),
    path('listing',views.listing,name=''),
    path('add_review',views.add_review,name='add_review'),
    path('order_details1/<booking>',views.order_details1,name='order_details1'),
    path('show_detail',views.show_detail,name='show_detail'),
    path('errorlisting',views.errorlisting,name=''),
    path('hostel-rooms/<hostel>',views.hostel_name,name='hostel_room'),
    path('hostel-rooms',views.rooms,name=''),
    path('booking',views.booking,name='booking'),
    path('mybookings',views.show_bookings,name="show_bookings"),
    path('transactions.html',views.trans,name='t'),
    path('comments',views.comment,name='comments'),
]
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
