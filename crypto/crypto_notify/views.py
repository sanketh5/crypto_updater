from django.http.response import HttpResponse
from django.shortcuts import render
import requests, json
from crypto_notify.bot_constants import *
from twilio.rest import Client

# Create your views here.
def home(request):
    return HttpResponse("Crypto ")

def api_call(coin_values):
    ''' the coin_vaues should be a string of asset_ids seperated by , eg. BTC,ETH,USD '''
    base_url = CRYPTO_API_URL
    headers = {'X-CoinAPI-Key' : CRYPTO_API_KEY}
    #add filter to url as get params
    url = base_url+"?filter_asset_id="+coin_values
    response = requests.get(url, headers=headers)
    if(response):
        required_coins = response.json()
        return required_coins
    else:
        return []

def display_coin_price(request):
    list_coins = api_call('BTC,ETH')
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

def message_sender(request):
    list_coins = api_call('BTC,ETH')
    usd_value_in_inr = get_current_usd_value('USD','INR')
    message_body = " \nUPDATE"
    for i in list_coins:
        coin_info = "\nID : "+str(i['asset_id'])+"\nNAME : "+i['name']+" \nPRICE : "+str(int(i['price_usd']*float(usd_value_in_inr)))+"USD \n"
        message_body+=coin_info 

    client = Client(TWILIO_ID, TWILIO_KEY)
    
    message_twilio = client.messages.create(
        body=message_body,
        from_ = TWILIO_NUMBER,
        to = '+917588425170'
    )
    print("message sent")
    return HttpResponse("sent")