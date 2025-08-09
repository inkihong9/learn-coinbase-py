# https://github.com/coinbase/coinbase-python

import os

from coinbase.rest import RESTClient

from json import dumps


coinbase_api_key = os.getenv('COINBASE_API_KEY')
coinbase_api_secret = os.getenv('COINBASE_API_SECRET')

client = RESTClient(coinbase_api_key, coinbase_api_secret)

all_accounts = client.get_accounts()
active_accounts = []

all_orders = client.list_orders()
for order in all_orders.orders:
    print(dumps(order.to_dict(), indent=2))
    # refer to order_sample.json for sample output
    

for account in all_accounts.accounts:
    print(dumps(account.to_dict(), indent=2))
    # refer to account_sample.json for sample output
    # difference between account.hold vs account.available_balance: account.hold refers to staked asset, while account.available_balance refers to amount available for trading or selling