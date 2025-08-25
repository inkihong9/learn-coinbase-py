import requests

from os import getenv as env
from cdp.auth.utils.jwt import generate_jwt, JwtOptions

# from coinbase import jwt_generator

USDC_ACCOUNT_ID = env('USDC_ACCOUNT_ID')

COINBASE_API_HOST = 'https://api.coinbase.com'
request_path = f"/v2/accounts/{USDC_ACCOUNT_ID}/transactions"

is_done = False

while not is_done:
    jwt_token = generate_jwt(JwtOptions(
        api_key_id=env('COINBASE_API_KEY_ED25519'),
        api_key_secret=env('COINBASE_API_SECRET_ED25519'),
        request_method='GET',
        request_host='https://api.coinbase.com',
        request_path=request_path,
        expires_in=120  # optional (defaults to 120 seconds)
    ))

    # print(jwt_token)

    # # For instructions generating JWT, check the "API Key Authentication" section
    JWT_TOKEN = jwt_token

    # Coinbase API base URL
    ENDPOINT_URL = f"{COINBASE_API_HOST}/{request_path}"

    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}"
    }

    # Make the API request
    response = requests.get(ENDPOINT_URL, headers=headers)

    response_body = response.json()

    request_path = response_body['pagination']['next_uri']

    is_done = True if request_path is None else False