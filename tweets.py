import random

#x keys
CONSUMER_KEY = 'my_key'
consumer_secret = 'my_consumer_secret'
access_token = 'my_access_toke'
access_token_secret = 'my_access_token_secret'

CONSUMER_KEY = 'my_key'
CONSUMER_SECRET = 'my_consumer_secret'
ACCESS_TOKEN = 'my_access_toke'
ACCESS_TOKEN_SECRET = 'my_access_token_secret'

# Authenticate to X
#AUTH = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
#API = tweepy.API(auth)

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

def fetch_latest_tweets():
    tweets = []
    for influencer in crypto_influencers:
        try:
            # Uncomment when Twitter API is set up
            #influencer_tweets = api.user_timeline(screen_name=influencer, count=5, tweet_mode='extended')
            #for tweet in influencer_tweets:
            #   tweets.append(f"{influencer}: {tweet.full_text}")
            pass  # Dummy pass when API is not set up
        except Exception as e:
            print(f"Error fetching tweets from {influencer}: {e}")   
    return tweets
