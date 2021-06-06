from django.contrib import admin

# Register your models here.
from .models import Coin_User,Coin
admin.site.register(Coin_User)
admin.site.register(Coin)