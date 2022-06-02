from django.contrib import admin
from django.urls import path
from .views import index,device,face

urlpatterns = [
    path('', index),
    path("device/",device),
    path("face/",face)

]
