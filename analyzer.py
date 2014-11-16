from Tweet import Tweet
import json
import glob
import io
import gzip
import db
import time
from mysql.connector.errors import IntegrityError
import operator

def getGzList(directory):
    # Return the list of files in data/ dir
    files = glob.glob(directory+'*.json.gz')
    return files

def getDay(json_gz):
    # Takes in a gzipped json file, decompresses in memory, and returns the original json
    f = open(json_gz, 'rb')
    c = io.BytesIO(f.read())
    d = gzip.GzipFile(fileobj=c)

    return d

def processDay(uncomp_json):
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

def findNewHashtags(tweets, currenttags):
    tags = []
    for tweet in tweets:
        tweettags = tweet.hashtags
        for tweettag in tweettags:
            if tweettag in tags or tweettag in currenttags:
                pass
            else:
                tags.append(tweettag)
    
    return tags

def findNewUsers(tweets, currentusers):
    users = []
    for tweet in tweets:
        if tweet.user_id in users or currentusers:
            pass
        else:
            users.append(tweet.user_id)

    return users

def main():
    # Get the list of files 
    files = getGzList('data/')
    day = getDay(files[0])
    
    # Make a db connection and the tables
    conn = db.makeConnection()
    cursor = db.makeCursor(conn)
    db.makeTables(cursor)

    # Get the tweets
    tweets = processDay(day)
    
    # Find new hashtags. Handle first run where db is empty
    try:
        currenthashtags = [item[1] for item in db.getHashtags(cursor)]
    except IndexError:
        currenthashtags = []
    newhashtags = findNewHashtags(tweets, currenthashtags)

    # Find new users. Handle first run where db is empty
    try:
        currentusers = [item for item in db.getUsers(cursor)]
    except IndexError:
        currentusers = []
    newusers = findNewUsers(tweets, currentusers)
    
    # Write new tags to the db
    for tag in newhashtags:
        cursor.execute('insert into hashtags (text) values (%s)', (tag,))
    conn.commit()
    
    # Write new users to the db
    for user in newusers:
        cursor.execute('insert into users (idUser) values (%s)', (user,))
    conn.commit()
    
    users = [item for item in db.getUsers(cursor)]
    hashtags = db.getHashtags(cursor)
    
    for tweet in tweets:
        cursor.execute('insert into tweets (idUser, tweetText, tweetDate, retweetCount, idTweet, cand_retweet, source_tweet_id) values (%s, %s, %s, %s, %s, %s, %s)', tweet.buildDbRow())
        if len(tweet.hashtags) != 0:
            tweet_hashtags = [(hashtag[0],tweet.tweet_id) for tag in tweet.hashtags for hashtag in hashtags if tag == hashtag[1]]
            for item in tweet_hashtags:
                cursor.execute('insert into tweet_hashtags (hashtag_id,tweet_id) values (%s,%s)', item)
        for user in tweet.user_mentions:
            cursor.execute('insert into user_mentions (mentioner, mentionee, tweet_id) values (%s,%s,%s)', (tweet.user_id, user, tweet.tweet_id))
    conn.commit()

    conn.close()
main()
