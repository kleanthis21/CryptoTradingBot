import time
from textblob import TextBlob
from binance.client import Client

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"


client = Client(API_KEY, API_SECRET,base_url = "https://testnet.binance.vision")


def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Returns sentiment between -1 and 1

def get_portfolio():
    account = client.get_account()
    balances = account['balances']
    return balances  # Returns a list of assets and their amounts

def place_oco_order(symbol, quantity, stop_price, limit_price):
    try:
        order = client.order_oco_sell(
            symbol=symbol,
            quantity=quantity,
            price=str(limit_price),
            stopPrice=str(stop_price),
            stopLimitPrice=str(stop_price * 0.99),  # Slightly lower stop-limit to ensure execution
            stopLimitTimeInForce='GTC'
        )
        print(f"OCO Order placed for {symbol}: {order}")
    except Exception as e:
        print(f"Error placing OCO order: {e}")

# buy coins based on sentiment analysis from textblob
def buy_based_on_sentiment(symbol, sentiment, portfolio_value):
    if sentiment >= 0.5:
        purchase_percentage = 15 + (sentiment - 0.5) * (30 - 15) / (1 - 0.5)
    elif sentiment > 0:
        purchase_percentage = 5
    else:
        purchase_percentage = 0

    if purchase_percentage > 0:
        amount_to_invest = portfolio_value * (purchase_percentage / 100)

        try:
            ticker = client.get_symbol_ticker(symbol=symbol)
            coin_price = float(ticker['price'])
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return

        quantity = amount_to_invest / coin_price

        try:
            # Instant buy first , so the oco trade will follow
            buy_order = client.order_market_buy(symbol=symbol, quantity=quantity)
            print(f"Bought {quantity} of {symbol} at price {coin_price}: {buy_order}")
        except Exception as e:
            print(f"Error placing market buy order: {e}")
            return

        place_oco_order(symbol, quantity, coin_price * 0.8, coin_price * 1.2)

def check_portfolio_and_sell(symbol):
    portfolio = get_portfolio()
    for asset in portfolio:
        if asset['asset'] == symbol.replace('USDT', '') and float(asset['free']) > 0:
            quantity = float(asset['free'])
            try:
                # Place a market sell order
                sell_order = client.order_market_sell(symbol=symbol, quantity=quantity)
                print(f"Sold {quantity} of {symbol} due to negative sentiment: {sell_order}")
            except Exception as e:
                print(f"Error placing market sell order: {e}")

# Main bot logic
def run_bot():
    coins = ["Bitcoin", "Dogecoin", "Ethereum,Solana"]  # Coins to track

    while True:
        tweets = get_mock_tweets()  # Replace with Twitter API call later

        for tweet in tweets:
            for coin in coins:
                if coin in tweet:
                    sentiment = analyze_sentiment(tweet)
                    print(f"Tweet: {tweet}")
                    print(f"Sentiment: {sentiment}")

                    symbol = coin.upper() + 'USDT'
                    portfolio_value = 1000  

                    if sentiment > 0:
                        buy_based_on_sentiment(symbol, sentiment, portfolio_value)
                    elif sentiment < 0:
                        check_portfolio_and_sell(symbol)
      
        time.sleep(180)

if __name__ == "__main__":
    run_bot()
