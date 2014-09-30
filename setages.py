import sqlite3
from random import randint
from random import choice

conn = sqlite3.connect('tweets.db')
cur = conn.cursor()

def getUsers(cursor):
    cursor.execute('select user_id from users')
    users = cursor.fetchall()
    return users

def setAge(users):
    for user in users:
        month = str(randint(1, 12))
        day = str(randint(1, 28))
        year = str(randint(1979, 1996))

        birthday = year+'-'+month+'-'+day+' 00:00:00.000'

        cur.execute('update users set age = (?) where user_id = (?)', (birthday,user[0]))
        print('inserting ' + birthday + ' into ' + user[0])
    conn.commit()

def setZip(users):
    zips = [ '61701','61702','61704','61705','61709','61710','61791','61799','61761','61790' ]
    for user in users:
        randzip = choice(zips)

        cur.execute('update users set zip = (?) where user_id = (?)', (randzip, user[0]))
        print('inserting ' + randzip + ' into ' + user[0])
    conn.commit()


users = getUsers(cur)
#setAge(users)
setZip(users)
conn.close()
