# https://github.com/coinbase/coinbase-python

import os, logging

from coinbase.rest import RESTClient

from models import Record, RecordType, AssetType

from json import loads

logging.basicConfig(level=logging.INFO)

records = []

with open('./records/records.json', 'r') as f:
    for record_raw in loads(f.read()):
        record = Record.from_dict(record_raw)
        records.append(record)


coinbase_api_key = os.getenv('COINBASE_API_KEY')
coinbase_api_secret = os.getenv('COINBASE_API_SECRET')

if not coinbase_api_key or not coinbase_api_secret:
    raise EnvironmentError('Please set the COINBASE_API_KEY and COINBASE_API_SECRET environment variables.')

rest_client = RESTClient(coinbase_api_key, coinbase_api_secret)

all_accounts = rest_client.get_accounts()
# active_accounts = []

all_orders = rest_client.list_orders()
# active_orders = []

non_cancelled_orders = [
    o for o in all_orders.orders
    if o.status != 'CANCELLED'
]

non_empty_accounts = [
    a for a in all_accounts.accounts 
    if float(a.available_balance['value']) > 0 or float(a.hold['value']) > 0
]

for order in non_cancelled_orders:
    # o = Order.from_dict(order.to_dict())
    # active_orders.append(o)
    logging.info(order)
    # refer to order_sample.json for sample output
    

for account in non_empty_accounts:
    logging.info(account)

    # print(dumps(account.to_dict(), indent=2))
    # refer to account_sample.json for sample output
    # difference between account.hold vs account.available_balance: account.hold refers to staked asset, 
    # while account.available_balance refers to amount available for trading or selling