from binance import place_order, place_oco_order, get_quantity_precision, get_portfolio
from sentiment import analyze_sentiment
from tweets import get_mock_tweets, fetch_latest_tweets, crypto_influencers
import time
import random
from utils import get_symbol

def buy_based_on_sentiment(symbol: str, sentiment: float, portfolio_value: float):
    if sentiment >= 0.5:
        purchase_percentage = 15
    elif sentiment > 0:
        purchase_percentage = 10
    else:
        purchase_percentage = 0

    if purchase_percentage > 0:
        amount_to_invest = portfolio_value * (purchase_percentage / 100)

        try:
            coin_price = get_coin_price(symbol)
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return

        quantity = amount_to_invest / coin_price
        precision = get_quantity_precision(symbol)
        
        if precision is not None:
            quantity = round(quantity, precision)      
        
        try:
            buy_order = place_order(symbol, quantity, 'BUY')
            print(f"Bought {quantity} of {symbol} at price {coin_price}")
        except Exception as e:
            print(f"Error placing market buy order: {e}")
            return

        place_oco_order(symbol, quantity, coin_price * 0.8, coin_price * 1.2)

def fetch_tweets_and_process():
    coins = ["Bitcoin", "BinanceCoin", "Ethereum", "Solana", "LiteCoin"]  

    while True:
        tweets = get_mock_tweets() #Should be replace with Twitter API call later----GET mock tweets for now
        # tweets = fetch_latest_tweets() #the actual call for tweet fetch from x 
        
        tweet = random.choice(tweets) 
         #for tweet in tweets: # uncomment in x retrieval of tweets
        for coin in coins:
            if coin in tweet:
                sentiment = analyze_sentiment(tweet) 
                print(f"Tweet: {tweet}")
                print(f"Sentiment: {sentiment}")

                symbol = get_symbol(coin) + 'USDT' 
                portfolio_value = 1000  # Placeholder for portfolio value

                if sentiment > 0:
                    buy_based_on_sentiment(symbol, sentiment, portfolio_value)
                elif sentiment < 0:
                    check_portfolio_and_sell(symbol, sentiment)
                
        time.sleep(60)

def check_portfolio_and_sell(symbol: str, sentiment: float):
    if sentiment >= -0.3:
        print("Sentiment is not low enough to sell. No action taken.")
        return
    portfolio = get_portfolio()
    for asset in portfolio:
        if asset['asset'] == symbol.replace('USDT', '') and float(asset['free']) > 0:
            quantity = float(asset['free'])
            try:
                sell_order = place_order(symbol, quantity, 'SELL')
                print(f"Sold {quantity} of {symbol} due to negative sentiment")
            except Exception as e:
                print(f"Error placing market sell order: {e}")

if __name__ == "__main__":
    fetch_tweets_and_process()
