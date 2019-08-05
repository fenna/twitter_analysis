""" module that cleans the raw data and puts the cleaned data in a normalized db """

__author__ = 'F.Feenstra'

from stop_words import get_stop_words
import re
import langid
import sqlite3
import tconfig
import sys


class Model:
    def __init__(self, cr, cc):
        self.conn_raw = cr
        self.conn_clean = cc
        self.cur_raw = self.conn_raw.cursor()
        self.cur_clean = self.conn_clean.cursor()
        self.table = ''

    def create(self):
        pass

    def select(self):
        pass

    def store(*row):
        pass

    def storage(self):
        rows = self.cur_raw.fetchall()
        for row in rows:
            self.store(*row)
        self.conn_clean.commit()
        print('{} {} inserted'.format(len(rows), self.table))



class Users(Model):
    def create(self):
        self.table = 'Users'
        self.cur_clean.execute('''CREATE TABLE IF NOT EXISTS Users (
	                      id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                          name TEXT)''')

    def select(self):
        self.cur_raw.execute('SELECT DISTINCT user_id, user FROM Tweets')

    def store(self, id, name):
        self.cur_clean.execute(''' INSERT OR IGNORE INTO Users
                            (id, name)
                            VALUES (?,?)''',
                            (id, name))

class Tweets(Model):
    def create(self):
        self.table = 'Tweets'
        self.cur_clean.execute('''CREATE TABLE IF NOT EXISTS Tweets
            (id INTEGER PRIMARY KEY,
             text TEXT,
             created_at DATE,
             user_id INTEGER)''')

    def select(self):
        self.cur_raw.execute('SELECT text, created_at, user_id FROM Tweets')

    def store(self, text, created_at, user_id):
        self.cur_clean.execute(''' INSERT OR IGNORE INTO Tweets
                             (text, created_at, user_id)
                             VALUES (?,?,?)''',
                             (clean_text(text), created_at, user_id))


def clean_text(text):
    """function to clean text: remove emoij, http links and stopwords """
    text = text.encode('ascii', 'ignore').decode('ascii') # remove emoij
    text = re.sub(r'@\S+', '', text) #remove @names
    text = re.sub(r'[0-9]', '', text)
    text = text.replace('RT', '')
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text) # remove urls
    text.strip()

    try:
        stopwords = get_stop_words(langid.classify(text)[0])
    except:
        stopwords = get_stop_words('en')

    text = ' '.join([word.lower() for word in re.split(r'\W+', text) if word not in stopwords]) #remove stopwords

    return text


def main():
    config = tconfig.get_config()
    #raw data connection
    conn_raw = sqlite3.connect(config['dbraw'])
    #clean data connection
    conn_clean = sqlite3.connect(config['dbclean'])

    #model the tables from raw data to clean data
    print('**** modeling ****')
    tweets = Tweets(conn_raw, conn_clean)
    tweets.create()
    tweets.select()
    tweets.storage()
    users = Users(conn_raw, conn_clean)
    users.create()
    users.select()
    users.storage()

    #close connections
    conn_clean.close()
    conn_raw.close()

if __name__ == '__main__':
    sys.exit(main())
