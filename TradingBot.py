import time
from textblob import TextBlob
from binance.spot import Spot as Client
from binance.error import ClientError
import random
import math
import tweepy
 
#x keys
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

crypto_influencers = [
    "@APompliano",     
    "@VitalikButerin", 
    "@cz_binance",     
    "@100trillionUSD", 
    "@aantonop",       
    "@saylor",         
    "@elonmusk",       
    "@TheCryptoLark",  
    "@PeterMcCormack", 
    "@WhalePanda"      
]

API_KEY = "pBnWV34uTdhQxBT3UjbQbXebDJwO4nazjaW0j5dU6TfM2vVuiRNOnkvYg8r9lrAA"
API_SECRET = "y7N8mAvrTeB6iNkGE286loelrTpuqx73jeg0e1gqNtpHqFu6vY1Gf95KzEE8HKmy"


client = Client(API_KEY, API_SECRET,base_url = "https://testnet.binance.vision")


mock_tweets = [
    "Wow, Bitcoin is going to the moon!",  
    "Ethereum is facing some serious issues.",  
    "BinanceCoin is performing okay.",  
    "Bitcoin dropped hard, time to sell!",  
    "Solana is the fastest blockchain out there. Scaling like crazy!" ,
    "BNB is killing it! Binance ecosystem growing stronger every day",
    "Solana network down again. How can we trust it to scale"
]

def get_mock_tweets():
    return mock_tweets

def get_symbol(coin_name):
    coin_mapping = {
        'bitcoin': 'BTC',
        'ethereum': 'ETH',
        'solana': 'SOL',
        'LiteCoin': 'LTC',
        'BinanceCoin': 'BNB',      
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
        order = client.new_oco_order(
            symbol=symbol,
            side="SELL",
            quantity=quantity,
            aboveType='LIMIT_MAKER',  # 
            belowType='STOP_LOSS_LIMIT',
            abovePrice=round(limit_price,2),
            belowPrice = round(stop_price,2),
            belowStopPrice = round(stop_price * 0.98,2),
            belowTimeInForce = 'GTC' # Good 'til Canceled
        )
        print(f"OCO Order placed for {symbol}: {order}")
    except Exception as e:
        print(f"Error placing OCO order: {e}")

def get_quantity_precision(symbol):
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

# buy coins based on sentiment analysis from textblob
def buy_based_on_sentiment(symbol, sentiment, portfolio_value):
    if sentiment >= 0.5:
        purchase_percentage = 15 
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
        precision = get_quantity_precision(symbol)
        
        if precision is not None:
            quantity = round(quantity, precision)      
        
        try:
            # Instant buy first, so the OCO trade will follow
            buy_order = client.new_order(symbol=symbol, side='BUY', type='MARKET', quantity=quantity)
            print(f"Bought {quantity} of {symbol} at price {coin_price}")
        except Exception as e:
            print(f"Error placing market buy order: {e}")
            return

        place_oco_order(symbol, quantity, coin_price * 0.8, coin_price * 1.2)

def fetch_latest_tweets():
    tweets = []
    for influencer in crypto_influencers:
        try:
            # Uncomment this block once ready to use the Twitter API
            influencer_tweets = api.user_timeline(screen_name=influencer, count=5, tweet_mode='extended')
            for tweet in influencer_tweets:
                tweets.append(f"{influencer}: {tweet.full_text}")
            
        except tweepy.TweepError as e:
            print(f"Error fetching tweets from {influencer}: {e}")
    
    return tweets

def check_portfolio_and_sell(symbol,sentiment):
    if sentiment >= -0.3:
        print("Sentiment is not low enough to sell. No action taken.")
        return
    portfolio = get_portfolio()
    for asset in portfolio:
        if asset['asset'] == symbol.replace('USDT', '') and float(asset['free']) > 0:
            quantity = float(asset['free'])
            try:
                sell_order = place_order(symbol, quantity,'SELL')
                print(f"Sold {quantity} of {symbol} due to negative sentiment")
            except Exception as e:
                print(f"Error placing market sell order: {e}")


def run_bot():
    coins = ["Bitcoin", "BinanceCoin", "Ethereum","Solana","LiteCoin"]  

    while True:
        tweets = get_mock_tweets()  # Replace with Twitter API call later
       # tweets = fetch_latest_tweets() 

        tweet = random.choice(tweets) 

        for coin in coins:
            if coin in tweet:
                sentiment = analyze_sentiment(tweet) 
                print(f"Tweet: {tweet}")
                print(f"Sentiment: {sentiment}")

                symbol = get_symbol(coin) + 'USDT' 
                portfolio_value = 1000  # Placeholder for your portfolio value that you want to be spent by the bot

                if sentiment > 0:
                    # Buy based on the sentiment analysis
                    buy_based_on_sentiment(symbol, sentiment, portfolio_value)
                elif sentiment < 0:
                    # Sell if sentiment is negative and you hold the coin
                    check_portfolio_and_sell(symbol,sentiment)
                
        # Sleep for 1 minute and search again for tweet
        time.sleep(60)
        
if __name__ == "__main__":
    run_bot()
