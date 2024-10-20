import time
from textblob import TextBlob
from binance.spot import Spot as Client
from binance.error import ClientError
import random
 

API_KEY = "pBnWV34uTdhQxBT3UjbQbXebDJwO4nazjaW0j5dU6TfM2vVuiRNOnkvYg8r9lrAA"
API_SECRET = "y7N8mAvrTeB6iNkGE286loelrTpuqx73jeg0e1gqNtpHqFu6vY1Gf95KzEE8HKmy"


client = Client(API_KEY, API_SECRET,base_url = "https://testnet.binance.vision")


mock_tweets = [
    "Wow, Bitcoin is going to the moon!",  # Positive sentiment
    "Ethereum is facing some serious issues.",  # Negative sentiment
    "Dogecoin is performing okay.",  # Neutral sentiment
    "Bitcoin dropped hard, time to sell!"  # Negative sentiment
]

def get_mock_tweets():
    return mock_tweets

def get_symbol(coin_name):
    coin_mapping = {
        'bitcoin': 'BTC',
        'ethereum': 'ETH',
        'solana': 'SOL',
        'dogecoin': 'DOGE',
        'ripple': 'XRP',      
    }
    
    return coin_mapping.get(coin_name.lower(), coin_name.upper())

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Returns sentiment between -1 and 1

def get_portfolio():
    account = client.account()
    balances = account['balances']
    return balances  

def place_order(symbol, quantity,site):
    try:
        # Place a market buy order
        order = client.new_order(
            symbol=symbol,
            side=site,
            type='MARKET',
            quantity=round(quantity,1)
        )
        print(f"Market buy order placed: {order}")
    except ClientError as e:
        print(f"Error occurred: {e.error_code} - {e.error_message}")

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
            ticker = client.ticker_price(symbol=symbol)
            coin_price = float(ticker['price'])
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return

        quantity = amount_to_invest / coin_price

        try:
            # Instant buy first , so the oco trade will follow
            buy_order = place_order(symbol,quantity,'BUY')
            print(f"Bought {quantity} of {symbol} at price {coin_price}: {buy_order}")
        except Exception as e:
            print(f"Error placing market buy order: {e}")
            return

        place_oco_order(symbol, quantity, coin_price * 0.8, coin_price * 1.2)

def check_portfolio_and_sell(symbol,sentiment):
    if sentiment >= -0.5:
        print("Sentiment is not low enough to sell. No action taken.")
        return
    portfolio = get_portfolio()
    for asset in portfolio:
        if asset['asset'] == symbol.replace('USDT', '') and float(asset['free']) > 0:
            quantity = float(asset['free'])
            try:
                sell_order = place_order(symbol, quantity,'SELL')
                print(f"Sold {quantity} of {symbol} due to negative sentiment: {sell_order}")
            except Exception as e:
                print(f"Error placing market sell order: {e}")

# Main bot logic
def run_bot():
    coins = ["Bitcoin", "Dogecoin", "Ethereum","Solana","Xrp"]  

    while True:
        tweets = get_mock_tweets()  # Replace with Twitter API call later

        tweet = random.choice(tweets) # get a random tweet from the mock tweets

        for coin in coins:
            if coin in tweet:
                sentiment = analyze_sentiment(tweet)  # Perform sentiment analysis
                print(f"Tweet: {tweet}")
                print(f"Sentiment: {sentiment}")

                symbol = get_symbol(coin) + 'USDT'  # Get trading symbol
                portfolio_value = 1000  # Placeholder for your portfolio value

                if sentiment > 0:
                    # Buy based on the sentiment analysis
                    buy_based_on_sentiment(symbol, sentiment, portfolio_value)
                elif sentiment < 0:
                    # Sell if sentiment is negative and you hold the coin
                    check_portfolio_and_sell(symbol,sentiment)
                
        # Sleep for 3 minutes (180 seconds) before the next run
        time.sleep(180)
        
if __name__ == "__main__":
    run_bot()
