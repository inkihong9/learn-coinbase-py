# https://github.com/coinbase/coinbase-python

import os
import json

from coinbase.wallet.client import Client

coinbase_api_key = os.getenv('COINBASE_API_KEY', 'my api key')
coinbase_api_secret = os.getenv('COINBASE_API_SECRET', 'my api secret')
client = Client(coinbase_api_key, coinbase_api_secret)

user = client.get_current_user()
# user_as_json_string = json.dumps(user)