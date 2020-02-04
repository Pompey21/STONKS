import json
import requests
import html

class Entry:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

        self.data = None

    def add_data(self, data):
        self.data = data
        
    @staticmethod
    def symbols(symbol_file, delim):
        with open(symbol_file, "r") as symbol_list:
            syms = [ (html.unescape(sym.split(delim)[0]), sym.split(delim)[1]) for sym in symbol_list ]

        return [ Entry(sym[0], sym[1][:-1]) for sym in syms ]

class Reader:
    def __init__(self, key_file, entries):
        with open(key_file, "r") as access_key:
            key = access_key.readline()[:-1]
            self.access_key = key

        self.entries = entries

    def pull(self):
        url = 'https://www.alphavantage.co/query'
        for entry in self.entries:
            payload = { 'function' : 'TIME_SERIES_DAILY',
                        'symbol'   : entry.symbol,
                        'apikey'   : self.access_key }

            entry.add_data(json.loads(requests.get(url, params = payload).text))
