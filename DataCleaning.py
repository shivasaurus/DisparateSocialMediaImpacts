#!/usr/bin/env python
# coding: utf-8




import sklearn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing as prep




def getAllData():
    # posts
    allPosts1 = pd.read_csv("allcrypto_postsToEnd2020.csv")[["normal_date", "one"]]
    allPosts2 = pd.read_csv("allcrypto_postsToMid2021.csv")[["normal_date", "one"]]
    allPosts3 = pd.read_csv("allcrypto_postsToEnd2021.csv")[["normal_date", "one"]]
    allPosts4 = pd.read_csv("allcrypto_postsToMar2022.csv")[["normal_date", "one"]]
    allPosts = pd.concat([allPosts1, allPosts2, allPosts3, allPosts4], axis=0)
    idx = pd.date_range('2020-08-02', '2022-02-28')
    allDailyPosts = allPosts.groupby("normal_date").sum("one")
    allDailyPosts.index = pd.DatetimeIndex(allDailyPosts.index)
    allDailyPosts = allDailyPosts.reindex(idx, fill_value = 0)
    allDailyPosts.rename(columns={"one":"allPosts"}, inplace=True)
    print(allDailyPosts.columns)
    
    # tweets
    allTweets = pd.read_csv("allcrypto-twitter-verified.csv")
    allDailyTwts = allTweets.groupby("date").sum("tweet_count")
    allDailyTwts.index = pd.DatetimeIndex(allDailyTwts.index)
    allDailyTwts = allDailyTwts.reindex(idx, fill_value = 0)
    allDailyTwts.rename(columns={"tweet_count":"allTweet_count"}, inplace=True)
    
    allAugFeb21 = pd.read_csv("allTrendsAugFeb21.csv")
    allMarSep21 = pd.read_csv("allTrendsMarSep21.csv")
    allOctFeb22 = pd.read_csv("allTrendsOctFeb22.csv")
    allAugFeb21["Cryptocurrency"] *= 0.36 # renormalization factor since Google Trends is 1-100 scale and we have three periods with different peaks
    allOctFeb22["Cryptocurrency"] *= 0.63 # renormalization factor since Google Trends is 1-100 scale and we have three periods with different peaks
    
    allTrends = pd.concat([allAugFeb21, allMarSep21, allOctFeb22], axis=0)
    allModTrends = allTrends[1:]
    allModTrends["DayTime"] = pd.to_datetime(allModTrends["Day"])
    allModTrends = allModTrends.set_index("DayTime")
    allModTrends = allModTrends.rename_axis(None, axis=0)
    allData = pd.concat([allDailyTwts, allDailyPosts, allModTrends], axis=1)
    allData[["standardized_allTweets", "standardized_allPosts", "standardized_allTrends"]] = prep.StandardScaler().fit_transform(allData[['allTweet_count', 'allPosts', "Cryptocurrency"]])
    allData["standardized_allTweetsSq"] = allData["standardized_allTweets"] * allData["standardized_allTweets"]
    allData["standardized_allPostsSq"] = allData["standardized_allPosts"] * allData["standardized_allPosts"]
    allData["standardized_allTrendsSq"] = allData["standardized_allTrends"] * allData["standardized_allTrends"]
    return allData
    
    
def getShibaData():
    # collect twitter data and index by date
    tweets = pd.read_csv("shiba_twitter_full.csv")
    tweets["tweet_count"] = 1
    idx = pd.date_range('2020-08-02', '2022-02-28')
    dailyTwts = tweets.groupby("date").sum("tweet_count")
    dailyTwts.index = pd.DatetimeIndex(dailyTwts.index)
    dailyTwts = dailyTwts.reindex(idx, fill_value = 0)
    
    # collect transaction data and index by date
    transactions = pd.read_csv("shiba_transactions.csv")[["timestamp", "tx_count"]]
    idx = pd.date_range('2020-08-02', '2022-02-28')
    dailyTxs = transactions.groupby("timestamp").sum("tx_count")
    dailyTxs.index = pd.DatetimeIndex(dailyTxs.index)
    dailyTxs = dailyTxs.reindex(idx, fill_value = 0)
    
    price = pd.read_csv("SHIB-USD (1).csv")[["Date", "Close", "Volume"]]
    idx = pd.date_range('2020-08-02', '2022-02-28')
    dailyPrice = price.groupby("Date").sum("Volume")
    dailyPrice.index = pd.DatetimeIndex(dailyPrice.index)
    dailyPrice = dailyPrice.reindex(idx, fill_value = 0)
    
    posts1 = pd.read_csv("shiba_posts.csv")
    posts1["one"] = 1
    posts = posts1[["normal_date", "one"]]
    idx = pd.date_range('2020-08-02', '2022-02-28')
    dailyPosts = posts.groupby("normal_date").sum("one")
    dailyPosts.index = pd.DatetimeIndex(dailyPosts.index)
    dailyPosts = dailyPosts.reindex(idx, fill_value = 0)
    dailyPosts
    
    idx = pd.date_range('2020-08-02', '2022-02-28')
    trendsAugFeb21 = pd.read_csv("ShibaTrendsAugFeb21.csv")
    trendsAugFeb21.replace("<1", 0, inplace=True)
    trendsMarSep21 = pd.read_csv("ShibaTrendsMarSep21.csv")
    trendsMarSep21.replace("<1", 0, inplace=True)
    trendsOctFeb22 = pd.read_csv("ShibaTrendsOctFeb22.csv")
    trendsOctFeb22.replace("<1", 0, inplace=True)
    trendsAugFeb21["Shiba"] *= (0.02*0.56) # renormalization factor since Google Trends is 1-100 scale and we have three periods with different peaks
    trendsMarSep21["Shiba"] *= 0.56 # renormalization factor since Google Trends is 1-100 scale and we have three periods with different peaks
    allTrends = pd.concat([trendsAugFeb21, trendsMarSep21, trendsOctFeb22], axis=0)
    modTrends = allTrends[1:]
    modTrends["DayTime"] = pd.to_datetime(modTrends["Day"])
    modTrends = modTrends.set_index("DayTime")
    modTrends = modTrends.rename_axis(None, axis=0)
    modTrends.replace("<1", 0, inplace=True)
    
    allData = pd.concat([dailyTwts, dailyPrice, dailyPosts, dailyTxs, modTrends, getAllData()], axis=1)
    allData["standardized_trends"] = prep.StandardScaler().fit_transform(allData[["Shiba"]])
    allData["standardized_txs"] = prep.StandardScaler().fit_transform(allData[["tx_count"]])
    allData["standardized_tweets"] = prep.StandardScaler().fit_transform(allData[["tweet_count"]])
    allData["standardized_posts"] = prep.StandardScaler().fit_transform(allData[["one"]])
    allData["standardized_social"] = (allData["standardized_tweets"] + allData["standardized_posts"])/2
    allData["standardized_txSq"] = allData["standardized_txs"] * allData["standardized_txs"]
    allData["standardized_tweetsSq"] = allData["standardized_tweets"] * allData["standardized_tweets"]
    allData["standardized_postsSq"] = allData["standardized_posts"] * allData["standardized_posts"]
    allData["standardized_trendSq"] = allData["standardized_trends"] * allData["standardized_trends"]
    allData["standardized_price"] = prep.StandardScaler().fit_transform(allData[["Close"]])
    allData["smoothedClosingPrice"] = allData["Close"].sort_index(ascending=False).ewm(span=2).mean().sort_index(ascending=True)
    allData["standardized_smoothprice"] = prep.StandardScaler().fit_transform(allData[["smoothedClosingPrice"]])
    return allData


# In[4]:


def getDogeData():
    tweets = pd.read_csv("doge_twitter_full.csv")
    tweets["tweet_count"] = 1
    idx = pd.date_range('2020-08-02', '2022-02-28')
    dailyTwts = tweets.groupby("date").sum("tweet_count")
    dailyTwts.index = pd.DatetimeIndex(dailyTwts.index)
    dailyTwts = dailyTwts.reindex(idx, fill_value = 0)
    
    transactions = pd.read_csv("doge_transactions.csv")[["timestamp_day", "transaction_count"]]
    idx = pd.date_range('2020-08-02', '2022-02-28')
    dailyTxs = transactions.groupby("timestamp_day").sum("transaction_count")
    dailyTxs.index = pd.DatetimeIndex(dailyTxs.index)
    dailyTxs = dailyTxs.reindex(idx, fill_value = 0)
    
    price = pd.read_csv("DOGE-USD.csv")[["Date", "Close", "Volume"]]
    idx = pd.date_range('2020-08-02', '2022-02-28')
    dailyPrice = price.groupby("Date").sum("Volume")
    dailyPrice.index = pd.DatetimeIndex(dailyPrice.index)
    dailyPrice = dailyPrice.reindex(idx, fill_value = 0)
    
    posts1 = pd.read_csv("doge_posts.csv")
    posts1["one"] = 1
    posts = posts1[["normal_date", "one"]]
    
    idx = pd.date_range('2020-08-02', '2022-02-28')
    dailyPosts = posts.groupby("normal_date").sum("one")
    dailyPosts.index = pd.DatetimeIndex(dailyPosts.index)
    dailyPosts = dailyPosts.reindex(idx, fill_value = 0)
    
    idx = pd.date_range('2020-08-02', '2022-02-28')
    trendsAugFeb21 = pd.read_csv("DogeTrendsAugFeb21.csv")
    trendsAugFeb21.replace("<1", 0, inplace=True)
    trendsMarSep21 = pd.read_csv("DogeTrendsMarSep21.csv")
    trendsMarSep21.replace("<1", 0, inplace=True)
    trendsOctFeb22 = pd.read_csv("DogeTrendsOctFeb22.csv")
    trendsOctFeb22.replace("<1", 0, inplace=True)
    trendsAugFeb21["Dogecoin"] = trendsAugFeb21["Dogecoin"].astype(float)
    trendsAugFeb21["Dogecoin"] *= 0.99 # renormalization factor since Google Trends is 1-100 scale and we have three periods with different peaks
    trendsOctFeb22["Dogecoin"] *= 0.1 # renormalization factor since Google Trends is 1-100 scale and we have three periods with different peaks
    allTrends = pd.concat([trendsAugFeb21, trendsMarSep21, trendsOctFeb22], axis=0)
    modTrends = allTrends[1:]
    modTrends["DayTime"] = pd.to_datetime(modTrends["Day"])
    modTrends = modTrends.set_index("DayTime")
    modTrends = modTrends.rename_axis(None, axis=0)
    modTrends.replace("<1", 0, inplace=True)
    
    allData = pd.concat([dailyTwts, dailyPrice, dailyPosts, dailyTxs, modTrends, getAllData()], axis=1)
    allData["standardized_trends"] = prep.StandardScaler().fit_transform(allData[["Dogecoin"]])
    allData["standardized_txs"] = prep.StandardScaler().fit_transform(allData[["transaction_count"]])
    allData["standardized_tweets"] = prep.StandardScaler().fit_transform(allData[["tweet_count"]])
    allData["standardized_posts"] = prep.StandardScaler().fit_transform(allData[["one"]])
    allData["standardized_social"] = (allData["standardized_tweets"] + allData["standardized_posts"])/2
    allData["standardized_txSq"] = allData["standardized_txs"] * allData["standardized_txs"]
    allData["standardized_tweetsSq"] = allData["standardized_tweets"] * allData["standardized_tweets"]
    allData["standardized_postsSq"] = allData["standardized_posts"] * allData["standardized_posts"]
    allData["standardized_trendSq"] = allData["standardized_trends"] * allData["standardized_trends"]
    allData["standardized_price"] = prep.StandardScaler().fit_transform(allData[["Close"]])
    allData["smoothedClosingPrice"] = allData["Close"].sort_index(ascending=False).ewm(span=2).mean().sort_index(ascending=True)
    allData["standardized_smoothprice"] = prep.StandardScaler().fit_transform(allData[["smoothedClosingPrice"]])
    
    return allData
    
    
    


# In[7]:


def getBitcoinData():
    bitcoinTweets = pd.read_csv("bitcoin_twitter_full.csv")
    idx = pd.date_range('2020-08-02', '2022-02-28')
    bitcoinDailyTwts = bitcoinTweets.groupby("date").sum("tweet_count")
    bitcoinDailyTwts.index = pd.DatetimeIndex(bitcoinDailyTwts.index)
    bitcoinDailyTwts = bitcoinDailyTwts.reindex(idx, fill_value = 0)
    
    bitcoinTransactions = pd.read_csv("Bitcoin_Transactions.csv")[["timestamp_day", "transaction_count"]]
    idx = pd.date_range('2020-08-02', '2022-02-28')
    bitcoinDailyTxs = bitcoinTransactions.groupby("timestamp_day").sum("transaction_count")
    bitcoinDailyTxs.index = pd.DatetimeIndex(bitcoinDailyTxs.index)
    bitcoinDailyTxs = bitcoinDailyTxs.reindex(idx, fill_value = 0)
    
    bitcoinPrice = pd.read_csv("BTC-USD (1).csv")[["Date", "Close", "Volume"]]
    idx = pd.date_range('2020-08-02', '2022-02-28')
    bitcoinDailyPrice = bitcoinPrice.groupby("Date").sum("Volume")
    bitcoinDailyPrice.index = pd.DatetimeIndex(bitcoinDailyPrice.index)
    bitcoinDailyPrice = bitcoinDailyPrice.reindex(idx, fill_value = 0)
    
    bitcoinPosts = pd.read_csv("bitcoin_posts.csv")[["normal_date", "one"]]
    idx = pd.date_range('2020-08-02', '2022-02-28')
    bitcoinDailyPosts = bitcoinPosts.groupby("normal_date").sum("one")
    bitcoinDailyPosts.index = pd.DatetimeIndex(bitcoinDailyPosts.index)
    bitcoinDailyPosts = bitcoinDailyPosts.reindex(idx, fill_value = 0)
    bitcoinDailyPosts
    
    idx = pd.date_range('2020-08-02', '2022-02-28')
    bitcoinAugFeb21 = pd.read_csv("BitcoinTrendsAugFeb21.csv")
    bitcoinMarSep21 = pd.read_csv("BitcoinTrendsMarSep21.csv")
    bitcoinOctFeb22 = pd.read_csv("BitcoinTrendsOctFeb22.csv")
    bitcoinAugFeb21["Bitcoin"] *= 0.74 # renormalization factor since Google Trends is 1-100 scale and we have three periods with different peaks
    bitcoinOctFeb22["Bitcoin"] *= 0.49 # renormalization factor since Google Trends is 1-100 scale and we have three periods with different peaks
    
    bitcoinAllTrends = pd.concat([bitcoinAugFeb21, bitcoinMarSep21, bitcoinOctFeb22], axis=0)
    bitcoinModTrends = bitcoinAllTrends[1:]
    bitcoinModTrends["DayTime"] = pd.to_datetime(bitcoinModTrends["Day"])
    bitcoinModTrends = bitcoinModTrends.set_index("DayTime")
    bitcoinModTrends = bitcoinModTrends.rename_axis(None, axis=0)
    
    allData = pd.concat([bitcoinDailyTwts, bitcoinDailyPrice, bitcoinDailyPosts, bitcoinModTrends, bitcoinDailyTxs, getAllData()], axis=1)
    allData["standardized_price"] = prep.StandardScaler().fit_transform(allData[["Close"]])
    allData["standardized_trends"] = prep.StandardScaler().fit_transform(allData[["Bitcoin"]])
    allData["standardized_txs"] = prep.StandardScaler().fit_transform(allData[["transaction_count"]])
    allData["standardized_tweets"] = prep.StandardScaler().fit_transform(allData[["tweet_count"]])
    allData["standardized_posts"] = prep.StandardScaler().fit_transform(allData[["one"]])
    allData["standardized_social"] = (allData["standardized_tweets"] + allData["standardized_posts"] + allData["standardized_trends"])/3
    allData["standardized_txSq"] = allData["standardized_txs"] * allData["standardized_txs"]
    allData["standardized_tweetsSq"] = allData["standardized_tweets"] * allData["standardized_tweets"]
    allData["standardized_postsSq"] = allData["standardized_posts"] * allData["standardized_posts"]
    allData["standardized_trendSq"] = allData["standardized_trends"] * allData["standardized_trends"]
    allData["smoothedClosingPrice"] = allData["Close"].sort_index(ascending=False).ewm(span=2).mean().sort_index(ascending=True)
    allData["standardized_smoothprice"] = prep.StandardScaler().fit_transform(allData[["smoothedClosingPrice"]])
    
    
    return allData
    


# In[6]:


def getEthereumData():
    tweets = pd.read_csv("ethereum_twitter_full.csv")
    tweets["tweet_count"] = 1
    idx = pd.date_range('2020-08-02', '2022-02-28')
    dailyTwts = tweets.groupby("date").sum("tweet_count")
    dailyTwts.index = pd.DatetimeIndex(dailyTwts.index)
    dailyTwts = dailyTwts.reindex(idx, fill_value = 0)
    
    transactions = pd.read_csv("ethereum_transactions.csv")[["timestamp_day", "transaction_count"]]
    idx = pd.date_range('2020-08-02', '2022-02-28')
    dailyTxs = transactions.groupby("timestamp_day").sum("transaction_count")
    dailyTxs.index = pd.DatetimeIndex(dailyTxs.index)
    dailyTxs = dailyTxs.reindex(idx, fill_value = 0)
    
    price = pd.read_csv("ETH-USD.csv")[["Date", "Close", "Volume"]]
    idx = pd.date_range('2020-08-02', '2022-02-28')
    dailyPrice = price.groupby("Date").sum("Volume")
    dailyPrice.index = pd.DatetimeIndex(dailyPrice.index)
    dailyPrice = dailyPrice.reindex(idx, fill_value = 0)
    
    posts1 = pd.read_csv("ethereum-reddit.csv")
    posts1["one"] = 1
    posts = posts1[["normal_date", "one"]]
    
    idx = pd.date_range('2020-08-02', '2022-02-28')
    dailyPosts = posts.groupby("normal_date").sum("one")
    dailyPosts.index = pd.DatetimeIndex(dailyPosts.index)
    dailyPosts = dailyPosts.reindex(idx, fill_value = 0)
    
    idx = pd.date_range('2020-08-02', '2022-02-28')
    trendsAugFeb21 = pd.read_csv("EthereumTrendsAugFeb21.csv")
    trendsAugFeb21["Ethereum"] *= 0.52 # renormalization factor since Google Trends is 1-100 scale and we have three periods with different peaks
    trendsMarSep21 = pd.read_csv("EthereumTrendsMarSep21.csv")
    trendsOctFeb22 = pd.read_csv("EthereumTrendsOctFeb22.csv")
    trendsOctFeb22["Ethereum"] *= 0.47 # renormalization factor since Google Trends is 1-100 scale and we have three periods with different peaks
    allTrends = pd.concat([trendsAugFeb21, trendsMarSep21, trendsOctFeb22], axis=0)
    modTrends = allTrends[1:]
    modTrends["DayTime"] = pd.to_datetime(modTrends["Day"])
    modTrends = modTrends.set_index("DayTime")
    modTrends = modTrends.rename_axis(None, axis=0)
    
    allData = pd.concat([dailyTwts, dailyPrice, dailyPosts, dailyTxs, modTrends, getAllData()], axis=1)
    allData["standardized_trends"] = prep.StandardScaler().fit_transform(allData[["Ethereum"]])
    allData["standardized_txs"] = prep.StandardScaler().fit_transform(allData[["transaction_count"]])
    allData["standardized_tweets"] = prep.StandardScaler().fit_transform(allData[["tweet_count"]])
    allData["standardized_posts"] = prep.StandardScaler().fit_transform(allData[["one"]])
    allData["standardized_social"] = (allData["standardized_tweets"] + allData["standardized_posts"] + allData["standardized_trends"])/3
    allData["standardized_txSq"] = allData["standardized_txs"] * allData["standardized_txs"]
    allData["standardized_tweetsSq"] = allData["standardized_tweets"] * allData["standardized_tweets"]
    allData["standardized_postsSq"] = allData["standardized_posts"] * allData["standardized_posts"]
    allData["standardized_trendSq"] = allData["standardized_trends"] * allData["standardized_trends"]
    allData["standardized_price"] = prep.StandardScaler().fit_transform(allData[["Close"]])
    allData["smoothedClosingPrice"] = allData["Close"].sort_index(ascending=False).ewm(span=2).mean().sort_index(ascending=True)
    allData["standardized_smoothprice"] = prep.StandardScaler().fit_transform(allData[["smoothedClosingPrice"]])
    return allData


# In[ ]:




