from binance.spot import Spot as Client
from binance.error import ClientError
import math

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

client = Client(API_KEY, API_SECRET, base_url="https://testnet.binance.vision")

def place_order(symbol: str, quantity: float, side: str):
    try:
        order = client.new_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=round(quantity, 1)
        )
        print(f"Market {side} order placed: {order}")
    except ClientError as e:
        print(f"Error occurred: {e.error_code} - {e.error_message}")

def place_oco_order(symbol: str, quantity: float, stop_price: float, limit_price: float):
    try:
        order = client.new_oco_order(
            symbol=symbol,
            side="SELL",
            quantity=quantity,
            price=round(limit_price, 2),
            stopPrice=round(stop_price, 2),
            stopLimitPrice=round(stop_price * 0.98, 2),
            stopLimitTimeInForce='GTC'
        )
        print(f"OCO Order placed for {symbol}: {order}")
    except Exception as e:
        print(f"Error placing OCO order: {e}")

def get_quantity_precision(symbol: str) -> int:
    try:
        exchange_info = client.exchange_info()
        symbol_info = next((s for s in exchange_info['symbols'] if s['symbol'] == symbol), None)

        if symbol_info:
            filters = symbol_info['filters']
            step_size = next((f['stepSize'] for f in filters if f['filterType'] == 'LOT_SIZE'), None)

            if step_size:
                precision = int(round(-math.log(float(step_size), 10), 0))
                return precision
            else:
                print(f"Step size not found for {symbol}.")
                return None
        else:
            print(f"Symbol info not found for {symbol}.")
            return None
    except Exception as e:
        print(f"Error fetching exchange info: {e}")
        return None

def get_portfolio():
    account = client.account()
    balances = account['balances']
    return balances
