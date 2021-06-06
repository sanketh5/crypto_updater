from django.urls import path, include
from accounts import views
from .views import *

urlpatterns = [
    path('signup/',views.signup.as_view())
]