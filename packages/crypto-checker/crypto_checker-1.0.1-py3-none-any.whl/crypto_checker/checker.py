import requests

class CryptoChecker:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"

    def get_price(self, crypto_name):
        url = f"{self.base_url}/simple/price?ids={crypto_name}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        if crypto_name in data:
            return data[crypto_name]['usd']
        else:
            return None
