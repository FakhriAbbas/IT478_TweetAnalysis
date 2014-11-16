import mysql.connector
from mysql.connector import errorcode

tweets = "create table if not exists tweets (idUser bigint not null, tweetText varchar(140) not null, tweetDate datetime not null, retweetCount smallint not null, idTweet bigint not null primary key, source_tweet_id bigint null, cand_retweet boolean not null, constraint fk_tweets_user foreign key (idUser) references users(idUser))"

users = "create table if not exists users (idUser bigint not null primary key)"

hashtags = "create table if not exists hashtags (id int primary key not null auto_increment, text varchar(30))"

tweet_hashtags = "create table if not exists tweet_hashtags (hashtag_id int not null, tweet_id bigint not null, constraint fk_hashtag_id foreign key (hashtag_id) references hashtags(id), constraint fk_tweet_id foreign key (tweet_id) references tweets(idTweet))"

candidates = "create table if not exists candidates(id smallint primary key auto_increment, screen_name varchar(14))"

candidate_mentions = "create table if not exists candidate_mentions (user_id bigint not null, candidate_id smallint not null, tweet_id bigint not null, constraint fk_candidate_id foreign key (candidate_id) references candidates(id), constraint fk_candidate_mentions_tweet_id foreign key (tweet_id) references tweets(idTweet))"

user_mentions = "create table if not exists user_mentions (mentioner bigint not null, mentionee bigint not null, tweet_id bigint not null, constraint fk_user_mentioner foreign key (mentioner) references users(idUser), constraint fk_tweet_mentioner foreign key (tweet_id) references tweets(idTweet))"

def makeConnection():
    conn = mysql.connector.connect(user='twitter', password='politics', host='localhost', database='twitter')
    return conn

def makeCursor(conn):
    cursor = conn.cursor()
    return cursor

def closeConn(conn):
    conn.close()

def makeTables(cursor):
    cursor.execute(users)
    cursor.execute(tweets)
    cursor.execute(hashtags)
    cursor.execute(tweet_hashtags)
    cursor.execute(user_mentions)

def getHashtags(cursor):
    hashtags = []
    cursor.execute("select id, text from hashtags")
    for result in cursor:
        hashtags.append(result)
    return hashtags

def getUsers(cursor):
    users = []
    cursor.execute("select idUser from users")
    for result in cursor:
        users.append(result)
    return users
