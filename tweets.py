import random

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
