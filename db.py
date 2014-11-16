import mysql.connector
from mysql.connector import errorcode

users = "create table users (idUser bigint not null primary key, gender char(1) not null, age datetime not null, zipcode int(5) not null, city varchar(45) not null)"

tweets = "create table tweets (idUser bigint not null, tweetText varchar(140) not null, tweetDate datetime not null, retweetCount smallint not null, idTweet bigint not null primary key, sentimentScore double not null, constraint fk_tweets_user foreign key (idUser) references users (idUser))"

sentiment_staging_users = "create table sentiment_staging_users (idUser bigint not null primary key, gender char(1) not null, age datetime not null, zipcode int(5) not null, city varchar(45) not null, status varchar(45) null)"

sentiment_staging_tweets = "create table sentiment_staging_tweets (Sentiment_Staging_User_idUser bigint not null, tweetText varchar(140) not null, tweetDate datetime not null, retweetCount smallint not null, idTweet bigint not null primary key, sentimentScore double null, status varchar(45) null, constraint fk_tweets_staging_user foreign key (Sentiment_Staging_User_idUser) references sentiment_staging_users (idUser))"

user_index = "create index fk_Tweets_User_idx on tweets (idUser asc)"
staging_user_index = "create index fk_Sentiment_Staging_Tweets_Sentiment_Staging_User1_idx on sentiment_staging_tweets (Sentiment_Staging_User_idUser asc)"

def makeConnection():
    conn = mysql.connector.connect(user='it478', password='tweets', host='localhost', database='it478')
    return conn

def makeCursor(conn):
    cursor = conn.cursor()
    return cursor

def closeConn(conn):
    conn.close()

def makeTables(cursor):
    cursor.execute(users)
    cursor.execute(tweets)
    cursor.execute(sentiment_staging_users)
    cursor.execute(sentiment_staging_tweets)
    cursor.execute(user_index)
    cursor.execute(staging_user_index)

def getUsers(cursor):
    users = []
    cursor.execute("select idUser from users")
    for result in cursor:
        users.append(result)
    return users
