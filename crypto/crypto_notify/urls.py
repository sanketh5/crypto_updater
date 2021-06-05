from django.contrib import admin
from django.urls import path, include
from crypto_notify import views
from .views import *
urlpatterns = [
    path('', views.home),
    path('price',views.display_coin_price),
    path('send_message',views.message_sender),
    
]
