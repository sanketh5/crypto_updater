import requests

URL = "http://127.0.0.1:8000/send_message"

response = requests.get(URL)

print(response)