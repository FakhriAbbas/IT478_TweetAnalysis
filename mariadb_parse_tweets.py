import os
import json
from random import randint
from random import choice
import mysql.connector
from mysql.connector import errorcode

conn = mysql.connector.connect(user='lucas', password='ohjustpoutthen',
        host='localhost', database='it478')

tables = {}

tables['users'] = ("create table users (user_id bigint not null primary key, gender char(1), age datetime, zipcode int(5), city varchar(45))")

tables['tweets'] = ("create table tweets (user_id bigint not null, tweet_text varchar(165), date_tweeted datetime, retweet_count smallint, tweet_id bigint not null primary key, sentimentScore double, constraint fk_tweets_user foreign key (user_id) references users (user_id))")

tables['sentiment_staging_users'] = ("create table sentiment_staging_users (staging_user_id bigint not null primary key, gender char(1), age datetime, zipcode int(5), city varchar(45), status varchar(45))")

tables['sentiment_staging_tweets'] = ("create table sentiment_staging_tweets (staging_user_id bigint not null, tweet_text varchar(165), date_tweeted datetime, retweet_count smallint, tweet_id bigint not null primary key, sentimentScore double, status varchar(45), constraint fk_tweets_staging_user foreign key (staging_user_id) references sentiment_staging_users (staging_user_id))")

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

def setAge():
    month = str(randint(1, 12))
    day = str(randint(1, 28))
    year = str(randint(1979, 1996))
    birthday = year+'-'+month+'-'+day
    return birthday

def setZip():
    zips = {    '61701':'Bloomington',
                '61702':'Bloomington',
                '61704':'Bloomington',
                '61705':'Bloomington',
                '61709':'Bloomington',
                '61710':'Bloomington',
                '61791':'Bloomington',
                '61799':'Bloomington',
                '61761':'Normal',
                '61790':'Normal'        }

    randzip = choice(list(zips.keys()))
    return [randzip, zips[randzip]]

def processUsers(user_list):
    for user in user_list:
        with open('collected_tweets/'+user, 'r') as user_file:
            tweets = json.load(user_file)
            if len(tweets) == 0:
                print('skipping user: empty tweets')
            else:
                gender = setGender()
                rzip = setZip()
                age = setAge()
                cursor.execute('insert into users (user_id, gender, age, zipcode, city) values (%s,%s,%s,%s,%s)', (user, gender, age, rzip[0], rzip[1]))
                for tweet in tweets:
                    row = (user, tweet['text'], str('0'), tweet['retweet_count'], tweet['id_str'] )
                    cursor.execute('insert into tweets (user_id, tweet_text, date_tweeted, retweet_count, tweet_id) values (%s, %s, %s, %s, %s)', row)
        conn.commit()

userlist = getUserIDs('collected_tweets')
processUsers(userlist)

cursor.close()
conn.close()
