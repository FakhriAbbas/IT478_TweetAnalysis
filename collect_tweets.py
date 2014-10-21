import auth
import json
import time
import twitter

def getStoredUsers(user_file):
    users = []
    with open(user_file) as temp:
        for line in temp:
            users.append(int(line))

    return users

def getUserTimeline(user, twitter):
    timeline = twitter.statuses.user_timeline(user_id=user, count=100, include_rts=1)
    return timeline

def dumpTimeline(user, timeline):
    with open('collected_tweets/'+str(user), 'w') as user_dump:
        json.dump(timeline, user_dump)

def main():
    t = auth.createAuth()

    users = getStoredUsers('ISU_followers.txt')

    for user in users:
        # TODO: improve error handling when it comes to unescapted characters
        print(user)
        try:
            tl = getUserTimeline(user, t)
            dumpTimeline(user, tl)
        except twitter.api.TwitterHTTPError:
            print("Oops, these are probably protected tweets from user " + str(user))
        except:
            with open('error.log','a') as fail:
                fail.write("Unexpected error at" + str(user))

        time.sleep(4)

main()
