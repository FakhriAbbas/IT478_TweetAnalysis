from tweepy.streaming import StreamListener
import json
from datetime import date
import time

class SListener(StreamListener):
    # Override methods where necessary
    def __init__(self, api = None):
        # Keep track of deleted tweets for processing later
        self.deleted = open('deleted_tweets.log', 'a')
        self.errorlog = open('error.log', 'a')

    def on_data(self, data):
        if 'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print warning['message']
            return false

    def on_status(self, status):
        # Open a file with today's date and append to it any new tweets
        # Hopefully, this will automatically handle changing the file that is
        # written every day after 00:00
        with open('data/'+date.today().isoformat()+'.json','a') as day_tweets:
            day_tweets.write(status)
            print(status)
        return

    # Write to the error log or deleted tweets log when necessary
    def on_delete(self, status_id, user_id):
        self.deleted.write(str(status_id) + "\n")
        return

    def on_limit(self, track):
        self.errorlog.write('Number of undelivered tweets at ' + time.strftime('%Y%m%d-%H%M%S') + ": " + track + "\n")
        return

    def on_error(self, status_code):
        self.errorlog.write('Error occured at ' + time.strftime('%Y%m%d-%H%M%S') + ': ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        self.errorlog.write(time.strftime('%Y%m%d-%H%M%S') + "Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return
