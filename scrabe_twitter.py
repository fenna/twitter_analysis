#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tstore
import sys
import tconfig

# Variable for database to store raw tweets
config = tconfig.get_config()
db = tstore.Twitterdb(config['dbraw'])

#This is a basic listener that just stores the tweets.
class StdOutListener(StreamListener):

    def on_data(self, data):
        db.store(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    try:
        #This handles Twitter authetification and the connection to Twitter Streaming API
        l = StdOutListener()
        auth = OAuthHandler(config['api_key'], config['api_secret_key'])
        auth.set_access_token(config['token'], config['secret_token'])
        stream = Stream(auth, l)

        #This line filter Twitter Streams to capture data by the keywords
        print('filtering on: ', config['filter'])
        stream.filter(track=config['filter'])
    except:
        print('twitter download stopped')
