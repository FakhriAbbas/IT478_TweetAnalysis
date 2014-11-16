from Tweet import Tweet
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


    for user in user_list:
        with open('collected_tweets/'+user, 'r') as user_file:
            tweets = json.load(user_file)
            if len(tweets) == 0:
                print('skipping user: empty tweets')
            else:
                cursor.execute('insert into sentiment_staging_users (idUser, gender, age, zipcode, city) values (%s,%s,%s,%s,%s)', (user, gender, age, rzip[0], rzip[1]))
                for tweet in tweets:
                    row = (user, tweet['text'], str('0'), tweet['retweet_count'], tweet['id_str'], 'LOADED' )
                    cursor.execute('insert into sentiment_staging_tweets (Sentiment_Staging_User_idUser, tweetText, tweetDate, retweetCount, idTweet, status) values (%s, %s, %s, %s, %s)', row)
        
        conn.close()
main()
