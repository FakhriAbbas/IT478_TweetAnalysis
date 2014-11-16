from tweepy import Stream
from tweepy import OAuthHandler
import ConfigParser
from listener import SListener
import os

def getCreds(creds_file):
    config = ConfigParser.RawConfigParser()

    try:
        config.readfp(open(creds_file))
    except IOError as e:
            print "I/O error ({0}): ({1})".format(e.errno, e.strerror)
            exit(1)

    try:
            myConsumerKey = config.get('DEFAULT', 'CONSUMER_KEY')
            myConsumerSecret = config.get('DEFAULT', 'CONSUMER_SECRET')
            myToken = config.get('DEFAULT', 'OAUTH_TOKEN')
            myTokenSecret = config.get('DEFAULT', 'OAUTH_TOKEN_SECRET')
    except ConfigParser.NoSectionError as e:
            print "ConfigParser ({0})".format(e)
            exit(1)
    except ConfigParser.NoOptionError as e:
            print "ConfigParser ({0})".format(e)
            exit(1)

    creds = [ myConsumerKey, myConsumerSecret, myToken, myTokenSecret]

    return creds

def main():
    if os.path.exists('data') == False:
        os.mkdir('data')

    hashtags = ['#isu', '#illinoisstate', '#illinoisstateu', '@IllinoisStateU' ]

    creds = getCreds('creds.txt')

    auth = OAuthHandler(creds[0], creds[1])
    auth.set_access_token(creds[2], creds[3])

    l = SListener()
    stream = Stream(auth, l)
    try:
        stream.filter(track=hashtags)
    except:
        print('error')
        stream.disconnect()

main()
