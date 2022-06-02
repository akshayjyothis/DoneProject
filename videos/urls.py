from django.contrib import admin
from django.urls import path
from .views import index,device,audio

urlpatterns = [
    path('', index),
    path("device",device),
    path("audio",audio)

]
