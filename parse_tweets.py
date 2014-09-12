import os
import json
from random import randint
import sqlite3

conn = sqlite3.connect('tweets.db')
cur = conn.cursor()

cur.execute('''create table tweets
                (user_id text, tweet_text text, date_tweeted text,
                retweet_count integer, tweet_id text )''')

cur.execute('''create table users
                (user_id text, gender text)''')
conn.commit()

def getUserIDs(path):
    user_list = os.listdir(path)
    return user_list

def setGender():
    # Simulate a coin flip as for whether a user will be male or female
    coin = randint(0,1)
    gender = 'F'
    if coin == 0:
        gender = 'M'
    return gender

def processUsers(user_list):
    for user in user_list:
        with open('collected_tweets/'+user, 'r') as user_file:
            tweets = json.load(user_file)
            if len(tweets) == 0:
                print('skipping user: empty tweets')
            else:
                gender = setGender()
                cur.execute('insert into users values (?,?)', (user, gender))
                for tweet in tweets:
                    row = (user, tweet['text'], str('0'), tweet['retweet_count'], tweet['id_str'] )
                    cur.execute('insert into tweets values (?, ?, ?, ?, ?)', row)
        conn.commit()


userlist = getUserIDs('collected_tweets')
processUsers(userlist)
conn.close()
