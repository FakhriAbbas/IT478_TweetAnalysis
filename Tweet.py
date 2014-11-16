import re
import random

class Tweet:
    def __init__(self, tweet_json):
        self.tweet_json = tweet_json
        self.text = self.setText()
        self.user_id = self.setUser()
        self.tweet_id = self.setTweetID()
        self.date = self.setDate()
        self.retweet_count = self.setRetweetCount()
     
    def getJson(self):
        return self.tweet_json

    def setText(self):
        # Strip out any new lines that a user may have entered
        orig = self.tweet_json['text'].replace('\n','')
        indices = []
        try:
            for url in self.tweet_json['entities']['urls']:
                indices.append(url['indices'])
        except KeyError:
            pass
        try:
            for item in self.tweet_json['entities']['media']:
                indices.append(item['indices'])
        except KeyError:
            pass
        try:
            for tag in self.tweet_json['entities']['hashtags']:
                indices.append(tag['indices'])
        except KeyError:
            pass

        try:
            for user in self.tweet_json['entities']['user_mentions']:
                indices.append(user['indices'])
        except KeyError:
            pass

        remove = []
        for index in indices:
            remove.append(self.tweet_json['text'][index[0]:index[1]])

        for rm in remove:
            orig = orig.replace(rm, '').strip()
            #orig = re.sub('[^a-zA-Z]+','', orig)

        orig = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',orig)
        #orig = re.sub('[^a-zA-z\s]+','',orig)
        orig = orig.strip()
        return orig

    def getText(self):
        return self.text

    def setUser(self):
        return self.tweet_json['user']['id_str']

    def getUser(self):
        return self.user_id

    def setTweetID(self):
        return self.tweet_json['id_str']

    def getTweetID(self):
        return self.tweet_id
    
    def setDate(self):
        months =  [ "01"
                ,   "02"
                ,   "03"
                ,   "04"
                ,   "05"
                ,   "06"
                ,   "07"
                ,   "08"
                ,   "09"
                ,   "10"
                ,   "11"
                ,   "12" ]

        orig = self.tweet_json['created_at'].split(' ')
        
        month = random.choice(months)
        year = orig[5]
        day = str(random.randrange(0,28))
        time = orig[3]

        return year+'-'+month+'-'+day+' '+time

    def getDate(self):
        return self.date

    def setRetweetCount(self):
        return self.tweet_json['retweet_count']
    
    def getRetweetCount(self):
        return self.retweet_count

    def buildDbRow(self):
       db_row = (self.user_id, self.text, self.date, self.retweet_count, self.tweet_id, "LOADED")
       return db_row
