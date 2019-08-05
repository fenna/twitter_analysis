"""
module that counts the words from tweets
"""

import re
import langid
import sqlite3
from collections import Counter
import tconfig
import sys

def fetch(config):
    """ function that fetches the tweets """
    conn = sqlite3.connect(config['dbclean'])
    cur = conn.cursor()
    cur.execute('SELECT text FROM Tweets')
    rows = cur.fetchall()
    return rows

def countwords(rows):
    """ function that puts all the tweets in one string and counts words """
    text = ''
    for row in rows:
        text += row[0]
    return Counter(text.split())

def write2js(counts):
    """ this function is made by dr Chuck """
    x = sorted(counts, key=counts.get, reverse=True)
    highest = None
    lowest = None
    for k in x[:100]:
        if highest is None or highest < counts[k] :
            highest = counts[k]
        if lowest is None or lowest > counts[k] :
            lowest = counts[k]
    print('Range of counts:',highest,lowest)

    # Spread the font sizes across 20-100 based on the count
    bigsize = 80
    smallsize = 20

    fhand = open('tword.js','w')
    fhand.write("tword = [")
    first = True
    for k in x[:100]:
        if not first: fhand.write( ",\n")
        first = False
        size = counts[k]
        size = (size - lowest) / float(highest - lowest)
        size = int((size * bigsize) + smallsize)
        fhand.write("{text: '"+k+"', size: "+str(size)+"}")
    fhand.write( "\n];\n")
    fhand.close()

def main():
    """ main function """
    config = tconfig.get_config()
    rows = fetch(config)
    counts = countwords(rows)
    write2js(counts)

if __name__ == '__main__':
    sys.exit(main())
