import auth
import json

# Create the twitter object
t = auth.createAuth()
cur = -1

with open("ISU_followers.txt", "a") as ffile:
    while cur != 0:
        followers = t.followers.ids(screen_name="IllinoisStateU", cursor=cur, count=5000)
        for follower in followers['ids']:
            ffile.write(str(follower)+'\n')
        cur = followers['next_cursor']
