from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings # new
from django.conf.urls.static import static # new

urlpatterns = [
    path('Pay1',views.Pay1,name='Pay1'),
    path('handlerequest1/',views.handlerequest1,name='handlerequest1'),
    path('handlerequest/',views.handlerequest,name='handlerequest'),
]
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)