# Capstone project twitter analysis

Program to fetch twitter messages, analyse the word counts and visualize them with a word cloud

## Overview

![Workflow overview](schema.png)

## Requirements
The program is writte in Python3 with the following (externeral) packages:

* twitter-api
* tweepy
* yaml
* stop_words
* langid
* sqlite3
* collections

## Twitter api
In order to access Twitter Streaming API, we need to get 4 pieces of information from Twitter: API key, API secret, Access token and Access token secret. If you to https://apps.twitter.com/ and log in with your twitter credentials you can create a New App and get the API key credentials for yourself.

For the twitter API we need the tweepy library see https://tweepy.readthedocs.io/en/latest/.

## Change settings
The application uses serveral settings such as database name, search key words etc which can be easily changed in the settings file present in the project.

Open config.yaml and change the setting.

## Run the program

The following steps need to be done to run the programm

Check the config.yaml and change the following:
* twitter keys with your own keys
* required filter key words
* required names for the raw database and the clean database

after the configuration the program needs to download some tweets. This might take some time
and you might need to restart the program several times.
run the progam that downloads the tweets into a database with

    python3 scrabe_twitter.py

(NB this program uses modules tstore.py, tconfig.py)

Once the database is filled with some tweets some cleaning steps need to be performed. This can be done by

    python3 tmodel.py

The program generates some cleaned tweets and a more normalized database

Lastly we need to count the words in the tweets. We use a program that generates a js file (tword.js)
with word counts

    python3 tword.py

by the command line command open tword.htm a word cloud is depicted

## Author
* Fenna Feenstra

## Acknowledge

This project is derived from concepts published by dr Chuck http://www.dr-chuck.com
