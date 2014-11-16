from Tweet import Tweet
from User import User
import json
import os
import io
import gzip
import db
import time
from mysql.connector.errors import IntegrityError
import operator

def getFileList(directory):
    # Return the list of files in data/ dir
    files = os.listdir(directory)
    return files

def processUser(uncomp_json):
    tweets = []
    for line in uncomp_json:
        tweet = json.loads(str(line, 'utf-8'))

        new_tweet = Tweet(tweet)
        new_tweet.setText()
        new_tweet.setUser()
        new_tweet.setTweetID()
        new_tweet.setDate()
        new_tweet.setCandidateRetweet()
        new_tweet.setUserMentions()
        new_tweet.setHashtags()
        new_tweet.setSourceTweet()

        tweets.append(new_tweet)

    return tweets

def main():
    # Get the list of files 
    files = getFileList('collected_tweets/')
    
    # Make a db connection and the tables
    conn = db.makeConnection()
    cursor = db.makeCursor(conn)
    db.makeTables(cursor)
    
    # log errors and continue
    f = open('errors.log','w')
    users = [User(user) for user in files]

    for user in users:
        cursor.execute('insert into sentiment_staging_users (idUser, age, gender, zipcode, city) values (%s,%s,%s,%s,%s)', (user.buildDbRow()))

    for user in users:
        with open('collected_tweets/'+user.user_id, 'r') as user_file:
            tweets_json = json.load(user_file)
            tweets = [Tweet(tweet) for tweet in tweets_json]
            for tweet in tweets:
                row = tweet.buildDbRow()
                try:
                    cursor.execute('insert into sentiment_staging_tweets (Sentiment_Staging_User_idUser, tweetText, tweetDate, retweetCount, idTweet, status) values (%s, %s, %s, %s, %s, %s)', row)
                except:
                    f.write("Error at: " + row)
        conn.commit()

    conn.close()
    f.close()
main()
