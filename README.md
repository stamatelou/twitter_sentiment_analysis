<H1>Real-time twitter sentiment analysis with Spark Structured Streaming & Python </H1>

This project is a good start for those want to start learning Spark Structure Streaming in Python. <br>

<b> Input data:</b> Live tweets with a preselected keyword <br>
<b>Main model:</b> Data preprocessing and apply sentiment analysis on the tweets <br>
<b>Output:</b> A parquet file with all the tweets and their sentiment analysis scores (polarity and subjectivity) <br>

<img align="center"  width="90%" src="https://github.com/stamatelou/twitter_sentiment_analysis/blob/master/architecture.png">

This project consists of 3 parts: <br>

## Part 1: Stream tweets from the Twitter API using tweepy (twitter_connection.py) <br>
The user selects locally a keyword and gets back live streaming tweets that include this keyword
```
     from tweepy import OAuthHandler
     from tweepy import Stream
     from tweepy.streaming import StreamListener
         
     # Set up your credentials
     consumer_key='<CONSUMER_KEY
```
## Part 2: Preprocess the tweets using pyspark (Spark Structure Streaming)<br>

## Part 3: Apply sentiment analysis using textblob <br>



