import json
import requests
import numpy


with open('list_final', 'r') as symbols_file:
        symbols = [ symbol[0:len(symbol)-1] for symbol in symbols_file.readlines()]


print(symbols)
symbols = symbols[0:5]

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

testing_opens = []
testing_opens = opens('MSFT')
print(testing_opens)

testing_close = []
testing_close = close('MSFT')
print(testing_close)

