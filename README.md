<h1>Crypto Sentiment Trading Bot</h1>


<h2>Overview</h2>
This project is a Python-based trading bot designed to execute trades on Binance based on the sentiment of tweets from a predefined list of crypto influencers. 
The bot uses TextBlob for sentiment analysis and interacts with the Binance API to place OCO (One-Cancels-the-Other) trades.

The bot:

Checks Twitter accounts of ten crypto influencers every minute for tweets mentioning specific cryptocurrencies (e.g., Bitcoin, Dogecoin, Ethereum).
Performs sentiment analysis on the tweets using TextBlob.
Places a buy order if the sentiment is positive, with OCO conditions (20% up or 20% down).
If the sentiment is negative and the coin is already in the user's portfolio, it will sell the coin instantly.
This project is developed as part of my MSc diploma thesis for research and educational purposes.

<h2>Features</h2>
Fetches the latest tweets from a predefined list of crypto influencers (currently uses mock tweets for testing).
Analyzes the sentiment of tweets using the TextBlob library:
  i)Positive sentiment triggers a buy order.
 ii)Negative sentiment checks if the coin is in the user's portfolio, and if found, sells the coin.
Executes trades on the Binance testnet (no real funds used) using the Binance API.
Fully customizable for sentiment thresholds and portfolio management.

<h2>Prerequisites</h2>
Before you begin, ensure you have met the following requirements:
Python 3.7 installed on your machine
Binance Spot API (binance-connector library)
Twitter Developer API access
Binance API keys
TextBlob for sentiment analysis


<h2>Required Python Packages</h2>
Install the required dependencies using pip:
pip install textblob
pip install binance-connector
pip install tweepy

<h2>Additional Setup</h2>
After installing textblob, download the necessary corpora for sentiment analysis:
python -m textblob.download_corpora

<h2>Setup and Configuration</h2>
Twitter API Setup
Create a Twitter Developer account and generate API keys and tokens.
Set your API credentials in a .env file or directly in the code.

<h2>Binance API Setup</h2>
Sign up for a Binance account.
Go to the API Management section of your Binance account and generate an API key and secret.
Add the API keys to your .env file or the configuration section of the bot.

<h2>How to Use</h2>
<h3>Running the Bot</h3>
1)Clone The Repo:
git clone https://github.com/yourusername/crypto-sentiment-trading-bot.git

2)Add your Binance API keys and Twitter API credentials:
  Update the following fields in the script with your actual keys:
  # Binance API keys (testnet)
  API_KEY = "your_binance_api_key"
  API_SECRET = "your_binance_api_secret"
  
  # Twitter API keys
  consumer_key = 'your_twitter_consumer_key'
  consumer_secret = 'your_twitter_consumer_secret'
  access_token = 'your_twitter_access_token'
  access_token_secret = 'your_twitter_access_token_secret'
3)Define the influencers you want to track
4)Update the coins list with the names of coins you want to monitor in the bot logic.


<h2>Testing</h2>
Currently, the bot uses mock tweets to simulate tweet fetching. You can replace the get_mock_tweets function with actual Twitter API calls once you're ready to use live data:

<h2>Customization<h2></h2>
Sentiment Analysis: Adjust the sentiment thresholds in the buy_based_on_sentiment function to control how aggressive the bot is when purchasing or selling based on tweet sentiment.
Portfolio Value: Modify the portfolio_value variable to represent how much of your total balance you'd like to trade.

Disclaimer
This bot is not intended for live trading and should only be used for testing and learning purposes. If you decide to use it with real funds, please proceed with caution and understand the risks involved in automated trading.





