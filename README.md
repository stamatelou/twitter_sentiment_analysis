<H1>Real-time twitter sentiment analysis with Spark Structured Streaming & Python </H1>

This project is a good start for those want to start learning Spark Structure Streaming in Python. <br>

<b> Input data:</b> Live tweets with a preselected keyword <br>
<b>Main model:</b> Data preprocessing and apply sentiment analysis on the tweets <br>
<b>Output:</b> A parquet file with all the tweets and their sentiment analysis scores (polarity and subjectivity) <br>

![Architecture](https://github.com/stamatelou/twitter_sentiment_analysis/blob/master/architecture.png)

This project consists of 3 parts: <br>

Part 1: Stream tweets from the Twitter API using tweepy (twitter_connection.py) <br>
The user selects locally a keyword and gets back live streaming tweets that include this keyword

Part 2: Preprocess the tweets using pyspark (Spark Structure Streaming)<br>
Part 3: Apply sentiment analysis using textblob <br>



