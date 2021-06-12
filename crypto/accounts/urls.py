from django.urls import path, include
from accounts import views

import django.contrib.auth.urls
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/',views.register),
    path('login/',views.custom_login)
]