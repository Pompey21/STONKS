import json
import requests
import numpy


with open('list_final', 'r') as symbols_file:
	symbols = [ symbol[0:len(symbol)-1] for symbol in symbols_file.readlines()]


print(symbols)
symbols = symbols[0:3]

collection = {}

for symbol in symbols:
	payload = {'function' : 'TIME_SERIES_DAILY', 'symbol' : symbol, 'apikey' : 'GbKksEFF4yrVs6il55v6gwY5aVje5f0j'}
	r = requests.get('https://www.alphavantage.co/query', params = payload)
	collection[symbol] = json.loads(r.text)

#print(collection)

def opens(symbol):
	return [ float(data['1. open']) for data in collection[symbol]['Time Series (Daily)'].values() ]

def close(symbol):
	return [ float(data['4. close']) for data in collection[symbol]['Time Series (Daily)'].values() ]
	
'''
#print('Open')
opens = []
for data in collection['AAPL']['Time Series (Daily)'].values():
	opens.append(float(data['1. open']))

'''

#print(opens('AAPL'))
quit()

#print('Close')
closes = []
for data in testing1['Time Series (Daily)'].values():
	closes.append(float(data['4. close']))
#	print(data['4. close'])

difference = []

for i in range(len(opens)-1):
	difference.append(float(opens[i]) - float(closes[i]))

#print(difference)

percentages = [ diff / open for open, diff in zip(opens, difference) ]
#print(percentages)
