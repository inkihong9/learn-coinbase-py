from coinbase.rest import RESTClient
from cb_models import CbOrder
from db_conn import SessionLocal

import os, logging

logging.basicConfig(level=logging.INFO)

session = SessionLocal()


coinbase_api_key = os.getenv('COINBASE_API_KEY')
coinbase_api_secret = os.getenv('COINBASE_API_SECRET')
if not coinbase_api_key or not coinbase_api_secret:
    raise EnvironmentError('Please set the COINBASE_API_KEY and COINBASE_API_SECRET environment variables.')


rest_client = RESTClient(coinbase_api_key, coinbase_api_secret)


cb_orders = rest_client.list_orders()


for o in cb_orders.orders:
    cb_order = CbOrder(o)
    session.add(cb_order)
    session.commit()



print(f"Fetched {len(cb_orders.orders)} filled orders from Coinbase.")
