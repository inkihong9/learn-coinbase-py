from coinbase.rest import RESTClient
import os, logging

logging.basicConfig(level=logging.INFO)


coinbase_api_key = os.getenv('COINBASE_API_KEY')
coinbase_api_secret = os.getenv('COINBASE_API_SECRET')
if not coinbase_api_key or not coinbase_api_secret:
    raise EnvironmentError('Please set the COINBASE_API_KEY and COINBASE_API_SECRET environment variables.')


rest_client = RESTClient(coinbase_api_key, coinbase_api_secret)


cb_filled_orders = rest_client.list_orders()


print(f"Fetched {len(cb_filled_orders.orders)} filled orders from Coinbase.")
