import os
import json
from random import randint
import mysql.connector
from mysql.connector import errorcode

conn = mysql.connector.connect(user='lucas', password='ohjustpoutthen',
        host='localhost', database='it478')

tables = {}
tables['tweets'] = ("create table tweets (user_id bigint not null, tweet_text varchar(165), date_tweeted datetime, retweet_count smallint, tweet_id bigint not null primary key, sentimentScore double)")

tables['users'] = ("create table users (user_id bigint not null primary key, gender char(1), age datetime, zipcode int(5), city varchar(45))")

tables['sentiment_staging_users'] = ("create table users (staging_user_id bigint not null primary key, gender char(1), age datetime, zipcode int(5), city varchar(45), status varchar(45))")

tables['sentiment_staging_tweets'] = ("create table tweets (staging_user_id bigint not null, tweet_text varchar(165), date_tweeted datetime, retweet_count smallint, tweet_id bigint not null primary key, sentimentScore double, status varchar(45))")

cursor = conn.cursor()

for name, ddl in tables.items():
    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


cursor.execute('alter table tweets (constraint foreign key (user_id) references users (user_id))')
cursor.execute('alter table sentiment_staging_tweets foreign key staging_user_id references sentiment_staging_users(user_id)')

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
                cursor.execute('insert into users (user_id, gender) values (%s,%s)', (user, gender))
                for tweet in tweets:
                    row = (user, tweet['text'], str('0'), tweet['retweet_count'], tweet['id_str'] )
                    cursor.execute('insert into tweets (user_id, tweet_text, date_tweeted, retweet_count, tweet_id) values (%s, %s, %s, %s, %s)', row)
        conn.commit()

userlist = getUserIDs('collected_tweets')
processUsers(userlist)

cursor.close()
conn.close()
