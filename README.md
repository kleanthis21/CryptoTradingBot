<h1>Crypto Sentiment Trading Bot</h1>


<h2>Overview</h2>
This project is a Python-based trading bot designed to execute trades on Binance based on the sentiment of tweets from a predefined list of crypto influencers. 
The bot uses TextBlob for sentiment analysis and interacts with the Binance API to place OCO (One-Cancels-the-Other) trades.

The bot:

Checks Twitter accounts of five crypto influencers every three minutes for tweets mentioning specific cryptocurrencies (e.g., Bitcoin, Dogecoin, Ethereum).
Performs sentiment analysis on the tweets using TextBlob.
Places a buy order if the sentiment is positive, with OCO conditions (20% up or 20% down).
If the sentiment is negative and the coin is already in the user's portfolio, it will sell the coin instantly.
This project is developed as part of my MSc diploma thesis for research and educational purposes.

<h2>Features</h2>
Sentiment Analysis: Uses TextBlob to analyze tweet sentiment (range: -1 to 1).
Binance Integration: Automatically places buy/sell orders on Binance using the Binance API.
OCO Orders: Automatically sets OCO sell conditions (20% up or down).
Configurable Influencers and Coins: Easily update the list of influencers and cryptocurrencies to track.

<h2>Prerequisites</h2>
Before you begin, ensure you have met the following requirements:
Python 3.x installed on your machine
A Binance account with API access enabled
Twitter Developer API access
Binance API keys
A virtual environment for Python (recommended)

<h2>Required Python Packages</h2>
Install the required dependencies using pip:
pip install textblob
pip install python-binance
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

<h2>Configuration</h2>
Create a .env file in the root directory of your project and add the following variables:

BINANCE_API_KEY=your_binance_api_key
BINANCE_API_SECRET=your_binance_api_secret
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

<h2>How to Use</h2>
<h3>Running the Bot</h3>
To run the bot, simply execute the following command in your terminal:
python bot.py
The bot will:

Retrieve tweets from the predefined influencers every 3 minutes.
Perform sentiment analysis on each tweet.
Place buy orders if the sentiment is positive, or sell the coin from your portfolio if the sentiment is negative.

<h2>Testing</h2>
For testing purposes, you can use predefined tweet strings in the code instead of retrieving actual tweets. Just comment out the Twitter API call and replace it with sample text to simulate the tweet analysis and trade execution process.
sample_tweet = "Wow! Bitcoin is going to the moon!"

<h2>Modify Influencers and Coins</h2>
You can modify the list of influencers and cryptocurrencies in the bot’s configuration:
influencers = ['influencer1', 'influencer2', 'influencer3']
cryptos = ['BTC', 'DOGE', 'ETH']





