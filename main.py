# https://github.com/coinbase/coinbase-python

import os, logging

from coinbase.rest import RESTClient


from models import Account, Order

logging.basicConfig(level=logging.INFO)


coinbase_api_key = os.getenv('COINBASE_API_KEY')
coinbase_api_secret = os.getenv('COINBASE_API_SECRET')



if not coinbase_api_key or not coinbase_api_secret:
    raise EnvironmentError("Please set the COINBASE_API_KEY and COINBASE_API_SECRET environment variables.")

rest_client = RESTClient(coinbase_api_key, coinbase_api_secret)

all_accounts = rest_client.get_accounts()
active_accounts = []

all_orders = rest_client.list_orders()
active_orders = []

for order in all_orders.orders:
    o = Order.from_dict(order.to_dict())
    active_orders.append(o)
    logging.info(o)
    # refer to order_sample.json for sample output
    

for account in all_accounts.accounts:
    acct = Account.from_dict(account.to_dict())
    if acct.available_balance > 0 or acct.hold > 0:
        active_accounts.append(acct)
        logging.info(acct)

    # print(dumps(account.to_dict(), indent=2))
    # refer to account_sample.json for sample output
    # difference between account.hold vs account.available_balance: account.hold refers to staked asset, 
    # while account.available_balance refers to amount available for trading or selling