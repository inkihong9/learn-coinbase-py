from coinbase.rest import RESTClient
from cb_model.cb_order import CbOrder
from db_conn import SessionLocal
from sqlalchemy import select, desc, asc
from datetime import timedelta

import os, logging

logging.basicConfig(level=logging.INFO)

session = SessionLocal()


all_cb_orders = session.execute(select(CbOrder).order_by(asc(CbOrder.created_time))).scalars().all()


net_usd = 0
net_coin = 0


for o in all_cb_orders:
    if o.settled and o.product_id.__contains__('SOL'):
        total_usd_after_fees = o.total_value_after_fees
        total_coin_after_fees = o.filled_size
        side = o.side.value
        if side == 'BUY':
            net_usd -= total_usd_after_fees
            net_coin += total_coin_after_fees
        elif side == 'SELL':
            net_usd += total_usd_after_fees
            net_coin -= total_coin_after_fees
        print(f"order completion date/time = {o.last_fill_time.strftime('%Y-%m-%d %H:%M:%S')} | order side = {o.side.value} | usd amount = {total_usd_after_fees} | coin amount = {total_coin_after_fees}")


print(f"net usd = {net_usd}")
print(f"net coin = {net_coin}")
