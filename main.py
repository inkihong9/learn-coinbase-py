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
skip_cb_accounts = set()

while has_next:
    cb_accounts = rest_client.get_accounts(cursor=cursor)
    has_next = cb_accounts.has_next
    if has_next:
        cursor = cb_accounts.cursor
    
    cb_all_accounts.extend(cb_accounts.accounts)


cb_watchlist_accounts = [a for a in cb_all_accounts if a.currency in assets.keys() and a.name.endswith('Wallet')]
cb_watchlist_accounts_dict = { a.currency: a for a in cb_watchlist_accounts }
cb_filled_orders = rest_client.list_orders(order_status='FILLED', start_date='2025-01-01T00:00:00.000Z')
cb_products = rest_client.get_products(product_ids=['XRP-USD', 'ETH-USD', 'ADA-USD', 'DOT-USD', 'CRO-USD', 'SOL-USD'])
cb_products_dict = { p.product_id.split('-')[0]: p for p in cb_products.products }


for order in reversed(cb_filled_orders.orders):
    record = Record.from_cb_order(order)
    coin_key = record.coin.value
    if coin_key in assets:
        cb_product = cb_products_dict.get(coin_key)
        cb_account = cb_watchlist_accounts_dict.get(coin_key)
        asset = assets[coin_key]
        asset.latest_action = record.type
        if record.type == RecordType.SELL:
            asset.latest_sell_fiat_amount = record.fiat_amount
            asset.current_fiat_amount = record.fiat_amount
            asset.current_coin_amount = 0
            asset.net_profit = asset.latest_sell_fiat_amount - asset.invested_fiat_amount
            skip_cb_accounts.add(coin_key)
        else:
            asset.current_fiat_amount = 0
            asset.current_coin_amount = record.coin_amount
            asset.latest_buy_coin_amount = record.coin_amount
            skip_cb_accounts.remove(coin_key)

# iterate through the watchlist accounts and calculate the remaining values
for cb_account in cb_watchlist_accounts:
    coin_key = cb_account.currency
    if coin_key in assets and not skip_cb_accounts.__contains__(coin_key):
        cb_product = cb_products_dict.get(coin_key)
        asset = assets[coin_key]
        asset.current_coin_amount = float(cb_account.available_balance['value']) + float(cb_account.hold['value'])
        asset.current_fiat_amount = asset.current_coin_amount * float(cb_product.price)
        if asset.net_profit == 0:
            asset.net_profit = asset.current_fiat_amount - asset.invested_fiat_amount

# bid price = highest price buyers are willing to pay
# ask price = lowest price sellers are willing to accept
# spread = ask price - bid price


# print the dashboard
print("Coin | Invested Amount | Current USD Amount | Latest Sell USD Amount | Initial Coin Amount | Current Coin Amount | Latest Buy Coin Amount | Net Profit | Latest Action")
for asset in assets.values():
    col2 = f"{asset.invested_fiat_amount:.2f}".ljust(15, ' ')    # Invested Amount
    col3 = f"{asset.current_fiat_amount:.2f}".ljust(18, ' ')     # Current USD Amount
    col4 = f"{asset.latest_sell_fiat_amount:.2f}".ljust(22, ' ') # Latest Sell USD Amount
    col5 = f"{asset.initial_coin_amount:.8f}".ljust(19, ' ')     # Initial Coin Amount
    col6 = f"{asset.current_coin_amount:.8f}".ljust(19, ' ')     # Current Coin Amount
    col7 = f"{asset.latest_buy_coin_amount:.8f}".ljust(22, ' ')  # Latest Buy Coin Amount
    col8 = f"{asset.net_profit:.2f}".ljust(10, ' ')              # Net Profit
    col9 = asset.latest_action.value.ljust(13, ' ')              # Latest Action
    print(f"{asset.coin.value}  | {col2} | {col3} | {col4} | {col5} | {col6} | {col7} | {col8} | {col9}")


# print all account balances
# print("\n\n\n\nCoin     | Total Balance")
# for cb_account in cb_all_accounts:
#     col1 = f"{cb_account.currency}".ljust(8, ' ')
#     col2 = f"{(float(cb_account.available_balance['value']) + float(cb_account.hold['value']))}"
#     print(f"{col1} | {col2}")