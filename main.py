# https://github.com/coinbase/coinbase-advanced-py/

# refer to account_sample.json for sample output
# difference between account.hold vs account.available_balance: account.hold refers to staked asset, 
# while account.available_balance refers to amount available for trading or selling

from coinbase.rest import RESTClient
from models import Record, RecordType, Coin, Asset
from json import loads
import os, logging

logging.basicConfig(level=logging.INFO)

records = []
assets = {}


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
            asset.invested_fiat_amount = record.fiat_amount


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

# watchlist_accounts = rest_client.get_accounts().accounts
cb_watchlist_accounts = [a for a in cb_all_accounts if a.currency in assets.keys() and a.name.endswith('Wallet')]
cb_filled_orders = rest_client.list_orders(order_status='FILLED', start_date='2025-01-01T00:00:00.000Z')
cb_products = rest_client.get_products(product_ids=['XRP-USD', 'ETH-USD', 'ADA-USD', 'DOT-USD', 'CRO-USD', 'SOL-USD'])
cb_products_dict = {p.product_id.split('-')[0]: p for p in cb_products.products}


for order in reversed(cb_filled_orders.orders):
    record = Record.from_cb_order(order)
    coin_key = record.coin.value
    if coin_key in assets:
        asset = assets[coin_key]
        asset.latest_action = record.type
        asset.highest_fiat_amount = max(asset.highest_fiat_amount, record.fiat_amount)
        asset.highest_coin_amount = max(asset.highest_coin_amount, record.coin_amount)
        if record.type == RecordType.SELL:
            asset.current_fiat_amount = record.fiat_amount
            asset.current_coin_amount = 0
        else:
            asset.current_fiat_amount = 0
            asset.current_coin_amount = record.coin_amount
        asset.net_profit = asset.current_fiat_amount - asset.invested_fiat_amount

# iterate through the watchlist accounts and calculate the remaining values
for cb_account in cb_watchlist_accounts:
    coin_key = cb_account.currency
    if coin_key in assets:
        cb_product = cb_products_dict.get(coin_key)
        asset = assets[coin_key]
        asset.current_coin_amount = float(cb_account.available_balance['value']) + float(cb_account.hold['value'])
        asset.current_fiat_amount = asset.current_coin_amount * float(cb_product.price)

# bid price = highest price buyers are willing to pay
# ask price = lowest price sellers are willing to accept
# spread = ask price - bid price


# print the dashboard
print("Coin | Invested Amount | Initial Coin Amount | Current USD Amount | Highest USD Amount | Current Coin Amount | Highest Coin Amount | Net Profit | Latest Action")
for asset in assets.values():
    col2 = f"{asset.invested_fiat_amount:.2f}".ljust(15, ' ')
    col3 = f"{asset.initial_coin_amount:.8f}".ljust(19, ' ')
    col4 = f"{asset.current_fiat_amount:.2f}".ljust(18, ' ')
    col5 = f"{asset.highest_fiat_amount:.2f}".ljust(18, ' ')
    col6 = f"{asset.current_coin_amount:.8f}".ljust(19, ' ')
    col7 = f"{asset.highest_coin_amount:.8f}".ljust(19, ' ')
    col8 = f"{asset.net_profit:.2f}".ljust(10, ' ')
    col9 = asset.latest_action.value.ljust(12, ' ')
    print(f"{asset.coin.value}  | {col2} | {col3} | {col4} | {col5} | {col6} | {col7} | {col8} | {col9}")