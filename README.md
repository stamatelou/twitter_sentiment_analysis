<H1>Streaming twitter data in real-time and sentiment analysis with Spark Structured Streaming & Python </H1>

This project is a good start for those want to start learning Spark Structure Streaming in Python. <br>



<b> Input data:</b> Live tweets with a preselected keyword <br>
<b>Main model:</b> Data preprocessing and apply sentiment analysis on the tweets <br>
<b>Output:</b> A parquet file with all the tweets and their sentiment analysis scores (polarity and subjectivity) <br>

<img align="center"  width="90%" src="https://github.com/stamatelou/twitter_sentiment_analysis/blob/master/architecture.png">

We use Python version 3.7.6 and Spark version 2.4.7. We should be cautious on the versions that we use because different versions of Spark require a different version of Python. 

## Main Libraries
tweepy: create a live data streaming pipeline with Twitter <br>
pyspark: preprocess the twitter data (Python's Spark library) <br>
textblob: apply sentiment analysis on the twitter text data <br>


This project consists of 3 parts: <br>
## Part 1: Stream tweets from the Twitter Streaming API using tweepy (twitter_connection.py) <br>

Step 1:Setup necessary packages <br>

```
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json
```

To start, we are going to need some packages to help build our streaming script. Tweepy is an excellent Python package for interacting with the Twitter API. For this, we need a few classes from it: StreamListener and Stream (for building our stream) and OAuthHandler (for authentication on Twitter). You will need to register on Twitter for developer credentials that we’ll be inserting later. datetime and csvwill be used for handling the output and putting the tweets from our stream into a file.


 Create a listening socket in the local machine (server) with a predefined local IP address and a port.






Step 2: Listen for a connection client in a IP address and port on the client side of the connection.
Step 3: Authenticate the connection with the Streaming API based on the personal credentials.
Step 4: Start streaming tweet data objects with a user-defined keyword and language.
Step 5: Retrieve the text of each tweet 




The user selects locally a keyword and gets back live streaming tweets that include this keyword
```
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json

consumer_key='LovGCp4taXgOGclj9Wum2XEda'
consumer_secret='d2NhvrqiEhsp8iBBZ1zsN5fl79AOwr0DOktoNqzIC56bK5NCLG'
access_token ='1323237425498435584-9TGePmcG2nq56MmN71K5jh7TBWd1AX'
access_secret='nhLAqoCicm4FJXwRw75MeQTeXxRu9L0Us4RqVxXgQP9AQ'

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
          # add at the end "end_of_tweet" to facilitate preprocessing
          self.client_socket.send(str(msg['extended_tweet']['full_text'] +"end_of_tweet").encode('utf-8'))         
          print(msg['extended_tweet']['full_text'])
        else:
          # add at the end "end_of_tweet" to facilitate preprocessing
          self.client_socket.send(str(msg['text']+"end_of_tweet").encode('utf-8'))
          print(msg['text'])
        return True
    except BaseException as e:
        print("Error on_data: %s" % str(e))
    return True
  def on_error(self, status):
    print(status)
    return True

def sendData(c_socket, keyword):
  print('start sending data from client - Twitter to server - local machine')
  # authentication based on the credentials
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)
  # start sending data from the Streaming API 
  twitter_stream = Stream(auth, TweetsListener(c_socket))
  twitter_stream.filter(track = keyword, languages=["en"])

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
## Part 2: Preprocess the tweets using pyspark (Spark Structure Streaming)<br>

## Part 3: Apply sentiment analysis using textblob <br>



