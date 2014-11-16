import re
import random

class Tweet:
    def __init__(self, tweet_json):
        self.tweet_json = tweet_json
        self.text = ""
        self.user_id = ""
        self.tweet_id = ""
        self.date = ""
        self.db_row = ""
        self.gender = ""
        self.age  ""
        self.zipcode = 0
     
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
        day = random.randrange(0,28)
        time = orig[3]

        self.date = year+'-'+month+'-'+day+' '+time

    def getDate(self):
        return self.date

    def setGender(self):
        self.gender = random.choice("MF")

    def getGender(self):
        return self.gender

    def setAge(self):
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        year = str(random.randint(1979, 1996))
        self.birthday = year+'-'+month+'-'+day

    def getAge(self):
        return self.birthday

    def setZipcode(self):
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
        self.zipcode = randzip

    def buildDbRow(self):
       self.db_row = (self.user_id, self.text, self.date, self.retweet_count, self.tweet_id, self.candidate_retweet, self.source_tweet_id)
       return self.db_row
