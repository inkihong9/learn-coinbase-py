# NOTES:
# see https://docs.cdp.coinbase.com/coinbase-app/track-apis/accounts#list-accounts for list accounts REST API details

import requests

from os import getenv as env
from cdp.auth.utils.jwt import generate_jwt, JwtOptions

COINBASE_API_HOST = 'https://api.coinbase.com'


def get_accounts():
    endpoint = '/v2/accounts'
    all_accounts = []
    is_done = False

    # For instructions generating JWT, check the "API Key Authentication" section
    # API Key Authentication - https://docs.cdp.coinbase.com/coinbase-app/authentication-authorization/api-key-authentication
    while not is_done:
        jwt = generate_jwt(JwtOptions(
            api_key_id=env('COINBASE_API_KEY_ED25519'),
            api_key_secret=env('COINBASE_API_SECRET_ED25519'),
            request_method='GET',
            request_host=COINBASE_API_HOST,
            request_path=endpoint,
            expires_in=120  # optional (defaults to 120 seconds)
        ))

        # Coinbase API base URL
        endpoint = f"{COINBASE_API_HOST}/{endpoint}"
        headers = { "Authorization": f"Bearer {jwt}" }

        '''
        from here it needs to catch exception
        '''

        # Make the API request
        response = requests.get(endpoint, headers=headers)
        response_body = response.json()
        endpoint = response_body['pagination']['next_uri']
        is_done = not endpoint
        all_accounts.extend(response_body['data'])

    return all_accounts


if __name__ == '__main__':
    accounts = get_accounts()
    for a in accounts:
        print(a)
