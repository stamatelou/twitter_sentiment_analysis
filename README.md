<H1>Streaming twitter data in real-time and sentiment analysis with Spark Structured Streaming & Python </H1>

This project is a good start for those want to start learning Spark Structure Streaming in Python. <br>



<b> Input data:</b> Live tweets with a preselected keyword <br>
<b>Main model:</b> Data preprocessing and apply sentiment analysis on the tweets <br>
<b>Output:</b> A parquet file with all the tweets and their sentiment analysis scores (polarity and subjectivity) <br>

<img align="center"  width="90%" src="https://github.com/stamatelou/twitter_sentiment_analysis/blob/master/architecture.png">

This project will consist of multiple phases. The first phase of our project will be using Python 3.6 to set up a live data streaming pipeline with Twitter using the tweepy package and Spark using the pyspark library. The tag word we will use is 'Donald Trump.' Our President is in the news a lot, and it would be interesting to see what hash tag topics are be attached to tweets that contain his name
This project consists of 3 parts: <br>

## Part 1: Stream tweets from the Twitter API using tweepy (twitter_connection.py) <br>
The user selects locally a keyword and gets back live streaming tweets that include this keyword
```
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json

consumer_key='hidden'
consumer_secret='hidden'
access_token ='hidden'
access_secret='hidden'

class TweetsListener(StreamListener):
  def __init__(self, csocket):
      self.client_socket = csocket
  def on_data(self, data):
      try:
          msg = json.loads( data )
          print("new message")
          if "extended_tweet" in msg:
            self.client_socket.send(str(msg['extended_tweet']['full_text'] +"end_of_tweet").encode('utf-8'))
             
            print(msg['extended_tweet']['full_text'])
          else:
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
      print('sendData start')
      auth = OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_token, access_secret)
      twitter_stream = Stream(auth, TweetsListener(c_socket))
      twitter_stream.filter(track = keyword, languages=["en"])



if __name__ == "__main__":
    s = socket.socket()
    host = "0.0.0.0"    
    port = 5555
    s.bind((host, port))
    print('connection ready')
    s.listen(4)
    print('listening')
    c, addr = s.accept()
    print("Received request from: " + str( addr ) )
    sendData(c, keyword = ['piano'])
```
## Part 2: Preprocess the tweets using pyspark (Spark Structure Streaming)<br>

## Part 3: Apply sentiment analysis using textblob <br>



