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

class CachedReader(Reader):
    def __init__(self, key_file, entries, cache_file):
        self.cache_file = cache_file
        super().__init__(key_file, entries)


    # FIXME: this function is expecting perfect input, figure out what should be accepted or not
    def pull(self):
        with open(self.cache_file, "r") as cache_contents: 
            cache_text = cache_contents.read()
            if len(cache_text) == 0:
                return
            
            cache = json.loads(cache_text)
            for entry in self.entries:
                series_data = cache.get(entry.symbol).get('data')
                if series_data is None:
                    entry.add_data(series_data)
                        

    def fill_cache(self):
        url = 'https://www.alphavantage.co/query'

        cache = {}
        for entry in self.entries:
            payload = { 'function'   : 'TIME_SERIES_DAILY',
                        'symbol'     : entry.symbol,
                        'outputsize' : 'full',
                        'apikey'     : self.access_key }

            cache[entry.symbol] = {'name': entry.name,
                                   'data': json.loads(requests.get(url, params = payload).text)}

        with open(self.cache_file, "w") as cache_contents:
            cache_contents.write(json.dumps(cache))

    def cache_entries(self):
        with open(self.cache_file, "r") as cache_contents:
            cache_text = cache_contents.read()
            cache = json.loads(cache_text) if len(cache_text) > 0 else {}
            
                
            return [ Entry(data.get("name"), symbol) for symbol, data in cache.items() ]
