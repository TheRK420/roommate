from django.contrib.auth import login
from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings # new
from django.conf.urls.static import static # new
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.home,name='home'),
    path('home.html', views.homepage,name='listing'),
    path('add-listing.html', views.listing,name='listing1'),
    path('terms.html', views.terms,name='terms'),
    path('policy.html', views.policy,name='policy'),
    path('bookingpolicy', views.bookingpolicy,name='bookingpolicy'),
    path('newpassword',views.trypass,name='newpassword'),
    path('contact', views.contact,name='contact'),
    path('adding_contact', views.adding_contact,name='adding_contact'),
    path('register',views.register,name='register_email'),
    path('register.html',views.signup,name='register'),
    path('login',views.user_login,name='user_login'),
    path('vendorHome',views.vendorHome,name="vendorHome"),
    path('studentHome',views.studentHome,name="studentHome"),
    path('logout.html',views.user_logout,name='logout'),
    path('Resetpass',views.Resetpass),
    path('datauser',views.dataofuser ,name='datauser'),
    path('kyc',views.kyc,name='kyc'),
    path('setpass/<m>/', views.setpass, name='setpass'),
    path('activate-user/<uidb64>/<token>',views.activate_user, name='activate'),
    path('forgot/<email>',views.forgot_verify, name='forgot'),
    path('coming_soon',views.coming_soon, name='coming_soon'),
]
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
