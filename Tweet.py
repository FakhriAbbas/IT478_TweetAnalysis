import re

class Tweet:
    candidates = [  'tomcottonAR','PryorForSenate',
                    'MarkUdall','CoryGardner',
                    'joniernst','TeamBraley',
                    'Team_Mitch','AlisonForKY',
                    'BillCassidy','MaryLandrieu',
                    'ThomTillis','kayhagan' ]

    def __init__(self, tweet_json):
        self.tweet_json = tweet_json
        self.text = ""
        self.user_id = ""
        self.tweet_id = ""
        self.date = ""
        self.candidate_retweet = 0
        self.original_tweet = ""
        self.retweet_count = 0
        self.user_mentions = []
        self.hashtags = []
        self.db_row = ""
        self.source_tweet_id = ""
     
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
        self.text = orig

    def getText(self):
        return self.text

    def setUser(self):
        self.user_id = self.tweet_json['user']['id_str']

    def getUser(self):
        return self.user_id

    def setTweetID(self):
        self.tweet_id = self.tweet_json['id_str']

    def getTweetID(self):
        return self.tweet_id
    
    def setDate(self):
        months = {  "Jan":"01",
                    "Feb":"02",
                    "Mar":"03",
                    "Apr":"04",
                    "May":"05",
                    "Jun":"06",
                    "Jul":"07",
                    "Aug":"08",
                    "Sep":"09",
                    "Oct":"10",
                    "Nov":"11",
                    "Dec":"12" }

        orig = self.tweet_json['created_at'].split(' ')
        
        month = months[orig[1]]
        year = orig[5]
        day = orig[2]
        time = orig[3]

        self.date = year+'-'+month+'-'+day+' '+time

    def getDate(self):
        return self.date

    def setOriginalTweet(self):
        try:
            self.original_tweet = tweet_json['retweeted_status']['id_str']
        except KeyError:
            self.original_tweet = ""
            
    
    def setCandidateRetweet(self):
        discard = 0
        try:
            if self.tweet_json['retweeted_status']['user']['screen_name'] in self.candidates:
                discard = 1
        except KeyError:
            # KeyError because it wasn't a retweet
            pass

        self.candidate_retweet = discard

    def isCandidateRetweet(self):
        return self.candidate_retweet

    def setUserMentions(self):
        try:
            for mentionee in self.tweet_json['entities']['user_mentions']:
                self.user_mentions.append(mentionee['id_str'])
        except KeyError:
            pass

    def getUserMentions(self):
        return self.user_mentions

    def setHashtags(self):
        try:
            for item in self.tweet_json['entities']['hashtags']:
                self.hashtags.append(item['text'].lower())
        except KeyError:
            pass

    def getHashtags(self):
        return self.hashtags

    def buildDbRow(self):
       self.db_row = (self.user_id, self.text, self.date, self.retweet_count, self.tweet_id, self.candidate_retweet, self.source_tweet_id)
       return self.db_row

    def setSourceTweet(self):
        try:
           self.source_tweet_id = self.tweet_json['retweeted_status']['id_str']
        except KeyError:
           self.source_tweet_id = ""

    def getSourceTweet(self):
        return self.source_tweet_id
