import random

class User:
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
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.gender = self.setGender()
        self.age = self.setAge()
        self.zipcode = self.setZipcode()
        self.city = self.setCity()

    def setGender(self):
        return random.choice("MF")

    def getGender(self):
        return self.gender

    def setAge(self):
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        year = str(random.randint(1979, 1996))
        return year+'-'+month+'-'+day

    def getAge(self):
        return self.age

    def setZipcode(self):
        randzip = random.choice(list(self.zips.keys()))
        return randzip

    def setCity(self):
        return zips[self.zipcode]

    def getCity(self):
        return self.city

    def getZipcode(self):
        return self.zipcode

    def buildDbRow(self):
        return (self.user_id, self.age, self.gender, self.zipcode)
