from django.urls import path
from . import views
from .views import scan

urlpatterns = [
    path('', views.index),
    path('nmap',views.nmap),
    path('scanvus',views.scanvus),
    path('nuclei',views.nuclei),
    path('api/scan/', scan, name='scan'),
]