# https://github.com/coinbase/coinbase-advanced-py/

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

all_accounts = rest_client.get_accounts()
filled_orders = rest_client.list_orders(order_status='FILLED', start_date='2025-01-01T00:00:00.000Z')


for order in reversed(filled_orders.orders):
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
        # asset.current_fiat_amount = record.fiat_amount
        # asset.current_coin_amount = record.coin_amount
        # asset.latest_action = record.type
    # asset = assets
    # logging.info(order)
    # logging.info("")
    # o = Order.from_dict(order.to_dict())
    # active_orders.append(o)
    # logging.info(order)
    # refer to order_sample.json for sample output

print("Coin | Invested Amount | Initial Coin Amount | Current USD Amount | Highest USD Amount | Current Coin Amount | Highest Coin Amount | Net Profit | Latest Action")


for asset in assets.values():
    print(f"{asset.coin.value}  | {asset.invested_fiat_amount:.2f} | {asset.initial_coin_amount:.4f} | {asset.current_fiat_amount:.2f} | {asset.highest_fiat_amount:.2f} | {asset.current_coin_amount:.4f} | {asset.highest_coin_amount:.4f} | {asset.net_profit:.2f} | {asset.latest_action.value}")

logging.info("hello world")

# for account in non_empty_accounts:
    # logging.info(account)

    # print(dumps(account.to_dict(), indent=2))
    # refer to account_sample.json for sample output
    # difference between account.hold vs account.available_balance: account.hold refers to staked asset, 
    # while account.available_balance refers to amount available for trading or selling