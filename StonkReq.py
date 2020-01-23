import json
import requests
import numpy

payload = {'function' : 'TIME_SERIES_DAILY', 'symbol' : 'MSFT', 'apikey' : 'GbKksEFF4yrVs6il55v6gwY5aVje5f0j'}

r = requests.get('https://www.alphavantage.co/query', params = payload)

testing1 = json.loads(r.text)

print('Open')
opens = []
for data in testing1['Time Series (Daily)'].values():
	opens.append(data['1. open'])
	print(data['1. open'])	

print('Close')
closes = []
for data in testing1['Time Series (Daily)'].values():
	closes.append(data['4. close'])
	print(data['4. close'])

difference = []

for i in range(len(opens)-1):
	difference.append(float(opens[i]) - float(closes[i]))

print(difference)
