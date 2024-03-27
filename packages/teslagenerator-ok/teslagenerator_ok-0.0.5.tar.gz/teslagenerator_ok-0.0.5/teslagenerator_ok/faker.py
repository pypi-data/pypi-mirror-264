import json, random, os
def install(package): os.system("pip install %s" % package)
def generator(size=6, chars = None): return ''.join(random.choice(chars) for _ in range(size))
while True:
    try:
        from unidecode import unidecode
        break
    except ImportError:
        install("unidecode")
        continue
whitespace = ' \t\n\r\v\f'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
printable = digits + ascii_letters + punctuation + whitespace
CACHE_OF_DATA = {}
class FakerError(Exception):...

class Faker:
    def __init__(self, lang = 'vietnamese', gender = 'all', datatype='txt'):
        global CACHE_OF_DATA
        self.__names = None
        self.__attrib = None
        self.tmp: dict = {}
        self.called: list = []
        self.lang = lang
        self._gender = gender
        self.__path = os.path.dirname(__file__)
        firstname, lastname = None, None
        firstname = os.path.join(self.__path, 'data/%s/firstnames.txt' % lang)
        lastname = os.path.join(self.__path, 'data/%s/%s.%s' % (lang, gender, datatype))

        self.__first_names = {} 
        
        if "first_name" in CACHE_OF_DATA:
            self.__first_names = CACHE_OF_DATA["first_name"]
        else:
            self.__first_names = open(firstname, encoding='utf8').read().splitlines()
            CACHE_OF_DATA["first_name"] = self.__first_names
            
        if "names" not in CACHE_OF_DATA:
            with open(lastname, "r", encoding='utf8') as names:
                names = names.read()
                if datatype == 'txt':
                    self.__names = names.splitlines()
                    
                if datatype == 'json':
                    self.__names = json.load(names)
                
                CACHE_OF_DATA["names"] = self.__names
        else: 
            self.__names = CACHE_OF_DATA["names"]
            
    def first_name(self, unsigned = False)->str:
        r = random.choice(self.__first_names)
        self.called.append("firstname")
        if unsigned:
            r = unidecode(r)
        self.tmp['ufirst_name'] = unidecode(r)
        self.tmp['first_name'] = r
        return r

    def last_name(self, unsigned = False)->str:
        r = random.choice(self.__names)
        self.called.append("lastname")
        rand = random.randint(1, 2)
        if rand == 1 and self.lang == "vietnamese" and "girl" in self._gender:
            r = "Thị "+ r
        if rand == 2 and self.lang == "vietnamese" and "boy" in self._gender:
            r = "Văn "+ r

        if unsigned:
            r = unidecode(r)
        self.tmp['ulast_name'] = unidecode(r)
        self.tmp['last_name'] = r
        return r

    def fullname(self, unsigned = False, returns = str):
        if "firstname" in self.called and "lastname" in self.called:
            first_name = self.tmp['ufirst_name'] if unsigned else self.tmp['first_name']
            last_name = self.tmp['ulast_name'] if unsigned else self.tmp['last_name']
        else:
            first_name = self.first_name(unsigned=unsigned)
            last_name = self.last_name(unsigned=unsigned)
        if unsigned:
            first_name = unidecode(first_name)
            last_name = unidecode(last_name)
        fullname = "%s %s" % (first_name, last_name)
        if returns == str:
            return fullname
        if returns == "delim": 
            return "%s:%s" % (first_name, last_name)
        if returns == tuple:
            return (first_name, last_name)

    def username(self, unsigned = True, ext = int, sep="_", range_ext = (1000, 2000))->str:
        first_name, last_name = self.fullname(unsigned=unsigned, returns="delim").replace(" ", sep).split(":")
        extension = None
        if range_ext != None:
            if ext == int:
                a,b = range_ext
                extension = random.randint(a,b)
            if ext == str:
                if type(range_ext) == tuple:
                    raise FakerError("ext: number, range_ext must be int")
                if type(range_ext) == float:
                    extension = generator(range_ext)
            username = "%s%s%s%s%s" %(first_name, sep, last_name, sep, extension)
        else:
            username = "%s%s%s" %(first_name, sep, last_name)

        if unsigned:
            username = unidecode(username)
        return username
    
    @classmethod
    @property
    def phone(cls):
        return generator(10, digits)
    
    @classmethod
    def generateUsername(cls, length: int = 20, sep="", chars=digits, lang="vietnamese", gender="all"):
        username = cls(lang=lang, gender=gender).username(range_ext=None, sep=sep)
        username_length = len(username)
        if username_length < length:
            username += generator(length - username_length, chars=chars)
        return username

    def email(self, server = "hotmail.com", sep="")->str:
        username = self.username(sep=sep)
        email =  str(username)+"@"+server
        return email

    @classmethod
    def generateInformation(cls, length = (15, 20), sep="_", chars=digits, lang="vietnamese", gender="all", birthday = (1990, 2008)):
        fakerInstance = cls(lang=lang, gender=gender)
        first_name = fakerInstance.first_name()
        last_name = fakerInstance.last_name()
        username = fakerInstance.username(sep=sep, range_ext=None)
        birthday = fakerInstance.birthday(min=birthday[0], max=birthday[1], returns=str)
        username_length = len(username)
        birthday = birthday.__attrib
        if username_length < length[0]:
            h = length[1] - username_length
            if h > 6:
                username = username+ birthday.replace("/", "")
            elif h > 4 and h <= 6:
                username = username+ ("".join(birthday.split("/")[2:]))
            elif h > 2 and h <= 4:
                username = username+ ("".join(birthday.split("/")[-1]))
            else:
                username = username+ str(birthday.split("/")[-1])[-2]
        
        return {
            "fullName": f"{first_name} {last_name}",
            "firstName": first_name,
            "lastName": last_name,
            "ufirstName": unidecode(first_name),
            "ulastName": unidecode(last_name),
            "username": username,
            "birthday": birthday
        }

    @staticmethod
    def gender():
        gender = random.choice(['male', "female", "other"])
        return gender

    @staticmethod
    def password(min = 10, max = 20, letters = ascii_letters):
        if type(min) != int and type(max) != int:
            raise FakerError("Min or max must be type int")
        if min > max:
            raise FakerError("Please set max mustbe over min number")
        lettors:str = letters
        if type(letters) == list:
            lettors = ""
            for letter in letters:
                lettors+=str(letter)
        password = generator(random.randint(min, max), chars=lettors)
        return password

    def birthday(self, min = 1990, max = 2006, returns = str, format = "dd/mm/yyyy"):
        month = random.randint(1, 12)
        year = random.randint(min, max)
        if month == 2 and year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            day = random.randint(1, 29)
        elif month == 2 and year % 4 !=0: 
            day = random.randint(1, 28)
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        elif month != 2: 
            day = random.randint(1, 30)

        if str == returns:
            formated = format
            if "d" in format:
                number_d = format.count("d")
                if number_d > 2:
                    raise FakerError("d must be format max 2")
                if number_d >1 and day < 10:
                    formated = formated.replace("d"*number_d, "0"*(number_d-1)+str(day))
                else:
                    formated = formated.replace("d"*number_d, str(day))
            if "m" in format:
                number_m = format.count("m")
                if number_m > 2:
                    raise FakerError("m must be format max 2")
                if number_m > 1 and month < 10:
                    formated = formated.replace("m"*number_m,"0"*(number_m-1)+str(month))
                else:
                    formated = formated.replace("m"*number_m,str(month) )
            if "y" in format:
                number_y = format.count("y")
                if number_y <=4 and number_y>0:
                    formated = formated.replace("y"*number_y,str(year)[-number_y:])
                else:
                    raise FakerError("Over format year: yyyy is incorectly!")
            self.__attrib = formated
            return self
        if list == returns: 
            return [day, month, year]
        if dict == returns:
            return {"day": day, "month": month, "year": year}
        if tuple == returns:
            return (day, month, year)

    def __str__(self) -> str:
        result = None
        if self.__attrib:
            result = self.__attrib
        return result
    

if __name__ == "__main__":
    new = Faker
    print(new.generateInformation())