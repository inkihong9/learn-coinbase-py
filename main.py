# https://github.com/coinbase/coinbase-advanced-py/

# refer to account_sample.json for sample output
# difference between account.hold vs account.available_balance: account.hold refers to staked asset,
# while account.available_balance refers to amount available for trading or selling

from client.account_client import get_accounts
from coinbase.rest import RESTClient
from models import Record, RecordType, Coin, Asset
from dashboard import print_dashboard as pd, print_aggregated_dashboard as pad
from json import loads
from datetime import datetime
import os, logging

logging.basicConfig(level=logging.INFO)

records = []
assets = {}


all_accounts_mine = get_accounts()


with open('./data/assets.json', 'r') as f:
    for asset_raw in loads(f.read()):
        asset = Asset.from_dict(asset_raw)
        coin_key = asset.coin.value
        assets[coin_key] = asset


with open('./data/records.json', 'r') as f:
    for record_raw in loads(f.read()):
        record = Record.from_dict(record_raw)
        records.append(record)
        coin_key = record.coin.value
        if coin_key in assets:
            asset = assets[coin_key]
            asset.initial_coin_amount = record.coin_amount
            asset.latest_buy_coin_amount = record.coin_amount
            asset.invested_fiat_amount = record.fiat_amount
            asset.latest_transaction_dt = record.created_at
            asset.buy_price = record.order_price


coinbase_api_key = os.getenv('COINBASE_API_KEY')
coinbase_api_secret = os.getenv('COINBASE_API_SECRET')
if not coinbase_api_key or not coinbase_api_secret:
    raise EnvironmentError('Please set the COINBASE_API_KEY and COINBASE_API_SECRET environment variables.')


rest_client = RESTClient(coinbase_api_key, coinbase_api_secret)
cb_all_accounts = []
has_next = True
cursor = None


while has_next:
    cb_accounts = rest_client.get_accounts(cursor=cursor)
    has_next = cb_accounts.has_next
    if has_next:
        cursor = cb_accounts.cursor
    cb_all_accounts.extend(cb_accounts.accounts)


cb_watchlist_accounts_dict = { a.currency: a for a in cb_all_accounts if a.name.endswith('Wallet') }
cb_filled_orders = rest_client.list_orders(order_status='FILLED', start_date='2025-01-01T00:00:00.000Z')
cb_products = rest_client.get_products()
cb_products_dict = { p.product_id.split('-')[0]: p for p in cb_products.products if p.watched }
usdc_acc = cb_watchlist_accounts_dict.get('USDC')


# step 1. iterate through the filled orders in chronological order
for cb_order in reversed(cb_filled_orders.orders):
    coin_key = cb_order.product_id.split('-')[0]
    asset = assets.get(coin_key)
    asset.latest_action = RecordType.BUY if cb_order.side == 'BUY' else RecordType.SELL
    asset.order_price = float(cb_order.average_filled_price)
    asset.latest_transaction_dt = datetime.strptime(cb_order.last_fill_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    if cb_order.side == 'BUY':
        asset.latest_buy_coin_amount = float(cb_order.filled_size)
        asset.buy_price = float(cb_order.average_filled_price)
    if cb_order.side == 'SELL':
        asset.latest_sell_fiat_amount = float(cb_order.total_value_after_fees)
        asset.sell_price = float(cb_order.average_filled_price)
        asset.current_fiat_amount = asset.latest_sell_fiat_amount


# step 2. iterate through the assets to retrieve the product price and account balance to
#         calculate the current coin amount, current fiat amount, and net profit
#         if asset's latest transaction date is before 2025-01-01
#             current_coin_amount = available balance + hold
#             current_fiat_amount = current_coin_amount * product.price
#             net_profit = current_fiat_amount - invested_fiat_amount
#         else if asset's latest transaction date is on or after 2025-01-01
#             current_coin_amount = available_balance + hold
#             net_profit = current_fiat_amount - invested_fiat_amount
for coin, asset in assets.items():
    cb_product = cb_products_dict.get(coin)
    cb_account = cb_watchlist_accounts_dict.get(coin)
    asset.current_coin_amount = float(cb_account.available_balance['value']) + float(cb_account.hold['value'])
    if asset.latest_transaction_dt < datetime(2025, 1, 1):
        asset.current_fiat_amount = asset.current_coin_amount * float(cb_product.price)
    asset.net_profit = asset.current_fiat_amount - asset.invested_fiat_amount
    asset.unit_price = float(cb_product.price)


# print the dashboard
pd(assets)
print("\n\n")
pad(assets, usdc_acc)
