from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import requests, json
from crypto_notify.bot_constants import *
from twilio.rest import Client
from django.contrib.auth.models import User
from crypto_notify.models import Coin_User,Coin
# Create your views here.
def home(request):
    return HttpResponse("Crypto ")

def api_call(coin_values, crypto_api_key = CRYPTO_API_KEY):
    ''' the coin_vaues should be a string of asset_ids seperated by , eg. BTC,ETH,USD '''
    base_url = CRYPTO_API_URL
    headers = {'X-CoinAPI-Key' : crypto_api_key}
    #add filter to url as get params
    url = base_url+"?filter_asset_id="+coin_values
    response = requests.get(url, headers=headers)
    print(f"the response form the server is  {response}")
    if(response):
        required_coins = response.json()
        return required_coins
    elif(response.status_code == 429):
        return api_call(coin_values, CRYPTO_API_KEY_2)
    else:
        return []

def display_coin_price(request,coins="BTC,ETH"):
    list_coins = api_call(coins)
    required_coin_prices = []
    for i in list_coins:
        temp = {}
        temp['id'] = i['asset_id']
        temp['name'] = i['name']
        temp['price'] = i['price_usd']
        required_coin_prices.append(temp)
    return render(request, 'crypto_notify/display_coin_price.html', {'coin_list':required_coin_prices})
        
def get_current_usd_value(from_currency, to_currency):
    '''can directly use this for getting crypto price'''
    main_url = BASE_URL_FOR_USD_VALUE + "&from_currency=" + from_currency + "&to_currency=" + to_currency+ "&apikey=" + USD_VALUE_API_KEY
    req_ob = requests.get(main_url)
    result = req_ob.json()
    return result["Realtime Currency Exchange Rate"]['5. Exchange Rate']

def message_sender(message,to_phone_number='+918788513442'):
    client = Client(TWILIO_ID, TWILIO_KEY)
    message_twilio = client.messages.create(
        body=message,
        from_ = TWILIO_NUMBER,
        to = to_phone_number
    )
    print(f"message sent to user \n\n {message}")
    return HttpResponse("MESSAGE SENT")

def auto_updater(request):
    if(request.method == 'GET'):
        list_users = User.objects.all()
        usd_value_in_inr = get_current_usd_value('USD','INR')
        for user_ in list_users:
            message =" \nUPDATE"
            coins_assosiated = Coin_User.objects.filter(user=user_)
            coin_ids = []
            coin_limit_price = {}
            for coin in coins_assosiated:
                if(coin.coin.coin_id not in coin_ids):
                    coin_ids.append(coin.coin.coin_id)
                coin_limit_price[coin.coin.coin_id +"_"+ coin.notify_type] = coin.price_limit
            coin_str = ",".join(coin_ids)
            coin_values_list = api_call(coin_str)
            for single_coin in coin_values_list:
                coin_id = single_coin['asset_id']
                current_coin_price_inr = float(usd_value_in_inr) * float(single_coin['price_usd'])
                if(coin_id + "_Down" in coin_limit_price.keys()):
                    coin_limit = coin_limit_price[coin_id+"_Down"]
                    difference = current_coin_price_inr - coin_limit
                    if(difference < coin_limit/100.0):
                        message+=("\nID : "+str(coin_id)+"\nNAME : "+single_coin['name']+" \nPRICE : "+str(int(current_coin_price_inr))+" INR \nTYPE : DOWN\n")
                if(coin_id + "_Up" in coin_limit_price.keys()):
                    coin_limit = coin_limit_price[coin_id+ "_Up"]
                    difference = coin_limit - current_coin_price_inr
                    if(difference < coin_limit/100.0):
                        message+=("\nID : "+str(coin_id)+"\nNAME : "+single_coin['name']+" \nPRICE : "+str(int(current_coin_price_inr))+" INR \nTYPE : UP\n")   
            if(message != " \nUPDATE"):
                message_sender(message)
        return HttpResponse("UPDATED")
    else:
        return HttpResponse("ONLY GET REQUEST IS ALLOWED")

            





