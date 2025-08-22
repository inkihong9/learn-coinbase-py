from models import RecordType
from coinbase.rest.types.accounts_types import Account

"""
prints a dashboard of assets with their details
"""
def print_dashboard(assets: dict):
    print("Coin | Unit Price | Initial Coin Amount | Current Coin Amount | Latest Buy Coin Amount | Buy Price | Invested Amount | Current USD Amount | Latest Sell USD Amount | Sell Price | Net Profit | Latest Action | Latest Transaction Date/Time (UTC)")
    for coin, asset in assets.items():
        unit_price            = f"{asset.unit_price:.2f}".ljust(10, ' ')                                 # Unit Price
        init_coin_amt         = f"{asset.initial_coin_amount:.8f}".ljust(19, ' ')                        # Initial Coin Amount
        curr_coin_amt         = f"{asset.current_coin_amount:.8f}".ljust(19, ' ')                        # Current Coin Amount
        latest_buy_coin_amt   = f"{asset.latest_buy_coin_amount:.8f}".ljust(22, ' ')                     # Latest Buy Coin Amount
        buy_price             = f"{asset.buy_price:.4f}".ljust(9, ' ')                                   # Buy Price
        invested_fiat_amt     = f"{asset.invested_fiat_amount:.2f}".ljust(15, ' ')                       # Invested Amount
        curr_fiat_amt         = f"{asset.current_fiat_amount:.2f}".ljust(18, ' ')                        # Current USD Amount
        latest_sell_fiat_amt  = f"{asset.latest_sell_fiat_amount:.2f}".ljust(22, ' ')                    # Latest Sell USD Amount
        sell_price            = f"{asset.sell_price:.4f}".ljust(10, ' ')                                 # Order Price
        net_profit            = f"{asset.net_profit:.2f}".ljust(10, ' ')                                 # Net Profit
        latest_action         = asset.latest_action.value.ljust(13, ' ')                                 # Latest Action
        latest_transaction_dt = asset.latest_transaction_dt.strftime("%Y-%m-%d %H:%M:%S").ljust(23, ' ') # Latest Transaction Date
        print(f"{coin}  | {unit_price} | {init_coin_amt} | {curr_coin_amt} | {latest_buy_coin_amt} | {buy_price} | {invested_fiat_amt} | {curr_fiat_amt} | {latest_sell_fiat_amt} | {sell_price} | {net_profit} | {latest_action} | {latest_transaction_dt}")


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