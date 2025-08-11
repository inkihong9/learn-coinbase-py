from coinbase import jwt_generator

import os

coinbase_api_key = os.getenv('COINBASE_API_KEY')
coinbase_api_secret = os.getenv('COINBASE_API_SECRET')

jwt_uri = jwt_generator.format_jwt_uri("GET", "/v2/prices/ETH-USD/buy")
jwt_token = jwt_generator.build_rest_jwt(jwt_uri, coinbase_api_key, coinbase_api_secret)

