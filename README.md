<H1>Real-time twitter sentiment analysis with Spark Structured Streaming & Python </H1>

This project is a good start for those want to start learning Spark Structure Streaming in Python. <br>

Input data: Live tweets with a preselected keyword
Main model: Data preprocessing and apply sentiment analysis on the tweets
Output: A parquet file with all the tweets and their sentiment analysis scores (polarity and subjectivity)

![Architecture](https://github.com/stamatelou/twitter_sentiment_analysis/blob/master/architecture.png)

This project consists of 3 steps:

Step 1: Stream tweets from the Twitter API using tweepy<br>
The user selects locally a keyword and gets back live streaming tweets that include this keyword

Step 2: Preprocess the tweets using pyspark (Spark Structure Streaming)<br>
Step 3: Apply sentiment analysis using textblob <br>



