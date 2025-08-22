from models import RecordType
from coinbase.rest.types.accounts_types import Account

"""
prints a dashboard of assets with their details
"""
def print_dashboard(assets: dict):
    print("Coin | Unit Price | Initial Coin Amount | Current Coin Amount | Latest Buy Coin Amount | Buy Price | Invested Amount | Current USD Amount | Latest Sell USD Amount | Sell Price | Net Profit | Latest Action | Latest Transaction Date")
    for coin, asset in assets.items():
        colA  = f"{asset.unit_price:.2f}".ljust(10, ' ')                                   # Unit Price
        col2  = f"{asset.initial_coin_amount:.8f}".ljust(19, ' ')                          # Initial Coin Amount
        col3  = f"{asset.current_coin_amount:.8f}".ljust(19, ' ')                          # Current Coin Amount
        col4  = f"{asset.latest_buy_coin_amount:.8f}".ljust(22, ' ')                       # Latest Buy Coin Amount
        col5  = f"{asset.buy_price:.4f}".ljust(9, ' ')                                     # Buy Price
        col6  = f"{asset.invested_fiat_amount:.2f}".ljust(15, ' ')                         # Invested Amount
        col7  = f"{asset.current_fiat_amount:.2f}".ljust(18, ' ')                          # Current USD Amount
        col8  = f"{asset.latest_sell_fiat_amount:.2f}".ljust(22, ' ')                      # Latest Sell USD Amount
        col9  = f"{asset.sell_price:.4f}".ljust(10, ' ')                                   # Order Price
        col10 = f"{asset.net_profit:.2f}".ljust(10, ' ')                                   # Net Profit
        col11 = asset.latest_action.value.ljust(13, ' ')                                   # Latest Action
        col12 = asset.latest_transaction_date.strftime("%Y-%m-%d %H:%M:%S").ljust(23, ' ') # Latest Transaction Date
        print(f"{coin}  | {colA} | {col2} | {col3} | {col4} | {col5} | {col6} | {col7} | {col8} | {col9} | {col10} | {col11} | {col12}")


def print_aggregated_dashboard(assets: dict, usdc_acc: Account):
    total_invested = sum(asset.invested_fiat_amount for asset in assets.values())
    total_fiat_amount = sum(asset.current_fiat_amount for asset in assets.values() if asset.latest_action == RecordType.BUY)
    total_usdc_balance = float(usdc_acc.available_balance['value']) + float(usdc_acc.hold['value'])
    total_fiat_value = total_fiat_amount + total_usdc_balance
    total_net_profit = sum(asset.net_profit for asset in assets.values())
    print("Aggregated Dashboard:")
    print(f"Total Invested Amount: ${total_invested:.2f}")
    print(f"Total USD Value (Coins only): ${total_fiat_amount:.2f}")
    print(f"Total USD Balance: ${total_usdc_balance:.2f}")
    print(f"Total USD Value: ${total_fiat_value:.2f}")
    print(f"Total Net Profit: ${total_net_profit:.2f}")