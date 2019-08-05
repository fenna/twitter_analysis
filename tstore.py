'''This module stores basic twitter data without cleaning '''

__author__ = 'F.Feensta'

import json
import sqlite3


class Twitterdb:
    def __init__(self, db):
        """ method that initializes the database """

        self.conn = sqlite3.connect(db)
        print("connected")
        self.cur = self.conn.cursor()
        print("cursor created")
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Tweets
            (id INTEGER PRIMARY KEY,
            created_at TEXT,
            tweet_id TEXT,
            id_str TEXT,
            text TEXT,
            source TEXT,
            user TEXT,
            user_id TEXT,
            reply_count INTEGER,
            retweet_count INTEGER,
            favorite_count INTEGER,
            lang TEXT)''')

    def store(self, tweet):
        """ method that stores the tweet (json) in a sqlite record """
        entry = json.loads(tweet)

        try:
            created_at = entry['created_at']
            tweet_id = entry['id']
            id_str = entry['id_str']
            text = entry['text']
            source = entry['source']
            user = entry['user']['screen_name']
            user_id = entry['user']['id']
            reply_count = int(entry['reply_count'])
            retweet_count = int(entry['retweet_count'])
            favorite_count = int(entry['favorite_count'])
            lang = entry['lang']

            self.cur.execute(''' INSERT OR IGNORE INTO Tweets
                             (created_at, tweet_id, id_str, text,
                             source, user, user_id, reply_count, retweet_count,
                             favorite_count, lang)
                             VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                             (created_at, tweet_id, id_str, text, source,
                              user, user_id, reply_count, retweet_count,
                              favorite_count, lang))

            self.conn.commit()
            print('inserted tweet', tweet_id)
        except:
            print('tweet skipped')

        def __del__(self):
            """ destructor: commits and closes the connection """
            self.conn.close()
