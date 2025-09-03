from coinbase.rest import RESTClient
from cb_models import CbOrder
from db_conn import SessionLocal
from sqlalchemy import desc
from datetime import timedelta

import os, logging

logging.basicConfig(level=logging.INFO)

session = SessionLocal()


last_order = session.query(CbOrder).order_by(desc(CbOrder.created_time)).first()
latest_order_datetime = None if not last_order else ((last_order.created_time) + timedelta(microseconds=1)).isoformat() + 'Z'


coinbase_api_key = os.getenv('COINBASE_API_KEY')
coinbase_api_secret = os.getenv('COINBASE_API_SECRET')
if not coinbase_api_key or not coinbase_api_secret:
    raise EnvironmentError('Please set the COINBASE_API_KEY and COINBASE_API_SECRET environment variables.')


# session.query(CbOrder).delete()


rest_client = RESTClient(coinbase_api_key, coinbase_api_secret)


cb_orders = rest_client.list_orders(start_date=latest_order_datetime)


for o in cb_orders.orders:
    cb_order = CbOrder(o)
    latest_order_datetime = o.created_time
    session.add(cb_order)


session.commit()



print(f"Fetched {len(cb_orders.orders)} orders from Coinbase.")
