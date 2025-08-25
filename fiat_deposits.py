import requests

from os import getenv as env
from cdp.auth.utils.jwt import generate_jwt, JwtOptions

# from coinbase import jwt_generator

USD_ACCOUNT_ID = env('USD_ACCOUNT_ID')
USDC_ACCOUNT_ID = env('USDC_ACCOUNT_ID')

COINBASE_API_HOST = 'https://api.coinbase.com'
request_path = f"/v2/accounts/{USDC_ACCOUNT_ID}/transactions"

is_done = False

all_deposits = []

deposit_amount = 0
interest_amount = 0

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

    deposits = [ t for t in response_body['data'] if t['type'] in ['buy','interest'] ]
    all_deposits.extend(deposits)

    request_path = response_body['pagination']['next_uri']

    is_done = True if request_path is None else False

for d in all_deposits:
    native_amount = float(d['native_amount']['amount'])
    if d['type'] == 'interest':
        interest_amount += native_amount
    elif d['type'] == 'buy':
        deposit_amount += native_amount
    print(d)

print(f"Total USD Amount from bank deposits: ${deposit_amount:.2f}")
print(f"Total USD Amount from interest: ${interest_amount:.2f}")