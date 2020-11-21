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