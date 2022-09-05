from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager


api_key = 'llx4btsRR0TLYiQe0WDsmkqyU8l9hhW3t0LiVKna1r9u88A2dkWyczkRGcOyMgnc'
api_secret = 'oPVFPv5SHrP6ZD8axomlKKo8lfSVet4YBq8Kk9XMkmoEvGK9MWMxl6s6JvY4Qrfg'
client = Client(api_key, api_secret)

prices = client.get_all_tickers()
print(prices)