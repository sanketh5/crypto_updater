from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Coin(models.Model):
    name =  models.CharField(max_length=600)
    coin_id = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Coin_User(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin,on_delete=models.CASCADE)
    price_limit = models.IntegerField(default=100)
    def __str__(self):
        return " | ".join([self.user.username,self.coin.name])