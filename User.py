import random

class User:
    user_id = ""
    gender = ""
    age = ""
    zipcode = 0

    def __init__(self, user_id):
        self.user_id = user_id
        self.gender = ""
        self.age = ""
        self.zipcode = ""

    def setGender(self):
        self.gender = random.choice("MF")

    def getGender(self):
        return self.gender

    def setAge(self):
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        year = str(random.randint(1979, 1996))
        self.age = year+'-'+month+'-'+day

    def getAge(self):
        return self.age

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

    def getZipcode(self):
        return self.zipcode
