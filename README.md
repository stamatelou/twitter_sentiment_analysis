<H1>Sentiment analysis on streaming twitter data in real-time using Spark Structured Streaming & Python </H1>

This project is a good start for those want to start learning Spark Structure Streaming in Python. <br>

Spark Structured Streaming/ Spark Streaming (why we chose the one and not the other?) 


<b> Input data:</b> Live tweets with a preselected keyword <br>
<b>Main model:</b> Data preprocessing and apply sentiment analysis on the tweets <br>
<b>Output:</b> A parquet file with all the tweets and their sentiment analysis scores (polarity and subjectivity) <br>

<img align="center"  width="90%" src="https://github.com/stamatelou/twitter_sentiment_analysis/blob/master/architecture.png">

We use Python version 3.7.6 and Spark version 2.4.7. We should be cautious on the versions that we use because different versions of Spark require a different version of Python. 

## Main Libraries
<b> tweepy:</b> interact with the Twitter Streaming API and create a live data streaming pipeline with Twitter <br>
<b> pyspark: </b>preprocess the twitter data (Python's Spark library) <br>
<b> textblob:</b> apply sentiment analysis on the twitter text data <br>

## Instructions
Run in a IDE locally the twitter_connection.py
First run the part one and let it running, and then run the part from a different IDE. 

This project consists of 3 parts: <br>
## Part 1: Stream tweets from the Twitter Streaming API using tweepy (twitter_connection.py) <br>

### <b>Step 1: </b> Setup the necessary packages <br>

```
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json
```
Tweepy library is necessary for connecting to the Twitter API and building the data streaming pipeline. We import its classes; StreamListener and Stream for building the stream and OAuthHandler for authenticating on Twitter. We import the socket module to create a communication channel between our local machine and the Twitter API and the json module to handle data of JSON objects.

### <b> Step 2: </b> Insert your credentials  <br>
```
consumer_key='hidden'
consumer_secret='hidden'
access_token ='hidden'
access_secret='hidden'
```
Use your developer credentials. If you do not have them yet, you will need to register on [Twitter for a developer account](https://developer.twitter.com/en/apply-for-access) and the request your credentials. 

### <b> Step 3: </b> Create a StreamListener instance <br>
```
class TweetsListener(StreamListener):
  # tweet object listens for the tweets
  def __init__(self, csocket):
    self.client_socket = csocket
  def on_data(self, data):
    try:  
      msg = json.loads( data )
      print("new message")
      # if tweet is longer than 140 characters
      if "extended_tweet" in msg:
        # add at the end "t_end" to facilitate preprocessing
        self.client_socket\
            .send(str(msg['extended_tweet']['full_text']+"t_end")\
            .encode('utf-8'))         
        print(msg['extended_tweet']['full_text'])
      else:
        # add at the end "t_end" to facilitate preprocessing
        self.client_socket\
            .send(str(msg['text']+"t_end")\
            .encode('utf-8'))
        print(msg['text'])
      return True
    except BaseException as e:
        print("Error on_data: %s" % str(e))
    return True
  def on_error(self, status):
    print(status)
    return True
```
The class TweetsListener represents a StreamListener instance, which contains one tweet per time. When we will activate the Stream, it creates the instance. The class consists of 3 methods; the on_data, the on_error, and the init. <br>
The <b>on_data</b> method of the TweetsListener receives all messages and defines which data to extract for each tweet from the Twitter Streaming API. Some examples could be the main message,comments,and hashtags. In our case we want to extract the text of the tweet. If we request the ['text'] field from each tweet, we will only receive the messages that are shorter than 140 characters. To always receive the full message, we need first to check if the tweet is longer than 140 charachetrs. If it is, we extract the ['extended_tweet']['full_text'] and if it is not we extract as before the ['text'] field. In the end of each tweet, we add the "t_end", so that we can identify easier the end of each tweet later. <br>
The <b>__init__</b> method initializes the socket of the Twitter Streaming API and the <b>on_error</b> method make sure that the stream works.

### <b> Step 4: </b> Sent data from Twitter <br>
```
def sendData(c_socket, keyword):
  print('start sending data from client to server')
  # authentication based on the credentials
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)
  # start sending data from the Streaming API 
  twitter_stream = Stream(auth, TweetsListener(c_socket))
  twitter_stream.filter(track = keyword, languages=["en"])
```
To start getting data from the Twitter API, we first authenticate the connection with the API based on our personal credentials as we defined in Step 2. After authentication, we start streaming tweet data objects with a pre-defined keyword and language. The objects returned are tweets, which belong to the TweetsListener class. 

### <b> Step 5:</b> Start Streaming <br>
```
if __name__ == "__main__":
    # server (local machine) creates listening socket
    s = socket.socket()
    host = "0.0.0.0"    
    port = 5555
    s.bind((host, port))
    print('socket is ready')
    # server (local machine) listens for connections
    s.listen(4)
    print('socket is listening')
    # return the socket and the address on the other side of the connection (client side)
    c_socket, addr = s.accept()
    print("Received request from: " + str(addr))
    # select here the keyword for the tweet data
    sendData(c_socket, keyword = ['piano'])
```
Before start streaming data from Twitter, we need to create a listening socket in the local machine (server) with a predefined local IP address and a port. Then, the socket listens for a connection client in a IP address and port on the client side of the connection. When we will run the script the client side of the connection will receive the data from the Twitter Streaming API. Here, we also select the keyword, which needs to be contained in the returned tweets.  

## Part 2: Preprocess the tweets using pyspark (sentiment_analysis.py)<br>

### <b>Step 1: </b> Setup the necessary packages <br>
```
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
from textblob import TextBlob
```
Pyspark is the Python API for Spark. Here, we use Spark Structured Streaming, which is a stream processing engine built on the Spark SQL engine and that's why we import the pyspark.sql module. We import it classes; SparkSession to create a stream sessions, functions and types to make available a list of build-in functions and data types accordingly. We also use textblob for the tweet data classification. 

### <b>Step 2: </b> Preprocessing the tweets <br>
```
def preprocessing(lines):
    words = lines.select(explode(split(lines.value, "t_end")).alias("word"))
    words = words.na.replace('', None)
    words = words.na.drop()
    words = words.withColumn('word', F.regexp_replace('word', r'http\S+', ''))
    words = words.withColumn('word', F.regexp_replace('word', '@\w+', ''))
    words = words.withColumn('word', F.regexp_replace('word', '#', ''))
    words = words.withColumn('word', F.regexp_replace('word', 'RT', ''))
    words = words.withColumn('word', F.regexp_replace('word', ':', ''))
    return words
```
Preprocess the tweets so that we can have only the tweet text. It receives in each batch many tweets from the Streaming Twitter API, and splits the tweets at the word "t_end". Then, it replaces the removes the empty rows and it applies regular expressions to clean up the tweet text. It removes the links (https://..), the usernames (@..), the hashtags (#), the string that indicates if the current tweet is a retweet (RT), and the character ":". 

### <b>Step 3: </b> Tweet classification <br>
```
# text classification
def polarity_detection(text):
    return TextBlob(text).sentiment.polarity
def subjectivity_detection(text):
    return TextBlob(text).sentiment.subjectivity
def text_classification(words):
    # polarity detection
    polarity_detection_udf = udf(polarity_detection, StringType())
    words = words.withColumn("polarity", polarity_detection_udf("word"))
    # subjectivity detection
    subjectivity_detection_udf = udf(subjectivity_detection, StringType())
    words = words.withColumn("subjectivity", subjectivity_detection_udf("word"))
    return words
```
Apply sentiment analysis using textblob to identify polarity and subjectivity scores within the range [0,1]. Since pyspark does not have a built-in function we used the user-defined function (udf) module to be able to apply the textblob function. 

### <b>Step 4: </b> Run the main function <br>
```
if __name__ == "__main__":
    # create Spark session
    spark = SparkSession.builder.appName("TwitterSentimentAnalysis").getOrCreate()

    # read the tweet data from socket
    lines = spark.readStream.format("socket").option("host", "0.0.0.0").option("port", 5555).load()
    # Preprocess the data
    words = preprocessing(lines)
    # text classification to define polarity and subjectivity
    words = text_classification(words)

    words = words.repartition(1)
    query = words.writeStream.queryName("all_tweets")\
        .outputMode("append").format("parquet")\
        .option("path", "./parc")\
        .option("checkpointLocation", "./check")\
        .trigger(processingTime='60 seconds').start()
    query.awaitTermination()
```
We first create an empty SparkSession, we connect it to the socket we made available in Part 1, and we load the batches with the tweet data locally. As soon as we receive the batch from the socket, we preprocess the received data, and then we apply the text classification to each tweet to define its polarity and subjectivity. Then, we collect all the tweets and save them in one file every minute (60 seconds) for efficient reads. The format of the saved file is parquet and to load it we downloaded the [ParquetFileViewer.exe](https://github.com/mukunku/ParquetViewer)



