#!/usr/bin/python
import bluetooth
import requests

url = 'http://127.0.0.1:8080/rest/items/phone1/state'

result = bluetooth.lookup_name('CC:20:E8:9F:83:17', timeout=5)

if (result != None):
    data = 'ON' 
else:
    data = 'OFF'

print(data)

response = requests.put(url, data=data)

