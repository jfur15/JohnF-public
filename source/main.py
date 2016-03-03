from source.question_answer import QA
from source.shape_checker import get_triangle_type, get_quadrilateral_type
import time
import difflib
import copy
import calendar
import math
import string
import source.git_utils
import sys, os.path
NOT_A_QUESTION_RETURN = "Was that a question?"
UNKNOWN_QUESTION = "I don't know, please provide the answer"
NO_QUESTION = 'Please ask a question first'
NO_TEACH = 'I don\'t know about that. I was taught differently'

def xpi(x):
    pi = "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348"
    return pi[int(x-1)]
    
def xfibo(x):
    x = int(x)
    if x < 2:
        return x
    else:
        return xfibo(x - 1) + xfibo(x - 2)

def sqrt(x):
    y = (float(1)/float(2))
    return str(round(math.pow(x,y),3))
    
def cbrt(x):
    y = (float(1)/float(3))
    return str(round(math.pow(x, y), 3))

def leapyear():
    nextyear = int(time.localtime()[0])
    nextyear += 1
    while calendar.isleap(nextyear) == False:
        nextyear += 1
    return str(nextyear)

class Interface(object):
    
    def __init__(self):
        self.how_dict = {}
        self.what_dict = {}
        self.where_dict = {}
        self.who_dict = {}

        self.keywords = ['How', 'What', 'Where', 'Who', "Why", "Is"]
        
        self.weight_units = {'pounds' : 453.59237 , 'ounces' :  28.3495231, 'grams' : 1, 'kilograms' : 100}

        self.length_units = {'feet' : 304.8, 'inches' : 25.4, 'centimeters' : 1 , 'meters' : 100, 'yards' : 914.4, 'miles' : 1609344}
        
        self.conversion_keywords = copy.deepcopy(self.weight_units)
        
        for unit in self.length_units:
            self.conversion_keywords[unit] = self.length_units[unit]

        self.question_mark = chr(0x3F)
        
        self.question_answers = {
            'What type of triangle is ': QA('What type of triangle is ', get_triangle_type),
            'What type of quadrilateral is ': QA('What type of quadrilateral is ', get_quadrilateral_type),
            'What time is it' : QA('What time is it', time.strftime("%c")),
            'What is digit X of pi': QA('What is digit X of pi', xpi),
            'What is digit X of fibonacci': QA('What is digit X of fibonacci', xfibo),
            'What is the square root of X': QA("What is the square root of X", sqrt),
            'What is the cubic root of X': QA("What is the cubic root of X", cbrt),
            'What is the next leap year': QA("What is the next leap year", leapyear),
            'What is my username': QA("What is my username", self.usernamecheck),
            'What unit do measure': QA("What unit do measure", self.unitcheck),
            'Is the FP in the repo': QA("Is the FP in the repo", source.git_utils.is_file_in_repo),
            'What is the status of FP': QA("What is the status of FP", source.git_utils.get_git_file_info),
            'What is the deal with FP': QA("What is the deal with FP", source.git_utils.get_file_info),
            'What branch is FP': QA("What branch is FP", source.git_utils.get_repo_branch),
            'Where did FP come from': QA("Where did FP come from", source.git_utils.get_repo_url),
        }
        
        self.last_question = None
        self.username = None
        
        self.command_answers = {
            'Please clear memory': QA('Please clear memory', self.__init__),
            'Open the door hal': QA('Open the door hal', self.haloutput),
            'Don\'t do anything': QA('Don\t do anything', "OK"),
        }

        
    def ask(self, question=""):
        if not isinstance(question, str):
            self.last_question = None
            raise Exception('Not A String!')
            
        if question in self.command_answers:
            answer = self.command_answers[question]
            if answer.function is None:
                return answer.value
            else:
                return answer.function()
        else:
            
            filepath = ""
            for keyword in question[:-1].split(' '):
                if keyword[0] == "/":
                    filepath = keyword
                    beforefirstslash = question.split( "/")[0]
                    afterfirstslash = question.split( "/", 1)[1]
                    
                    tempAfterList = afterfirstslash.split(' ')
                    
                    if len(tempAfterList) == 1:
                        afterfirstslash = "?"
                    else:
                        afterfirstslash = afterfirstslash.split(" ", 1)[1]
                        
                    question = beforefirstslash + afterfirstslash
                    
                    print question
                    print filepath
            if (question[-1] != self.question_mark or question.split(' ')[0] not in self.keywords):
                if question.split(' ')[0] == "Convert":
                    return self.conversion(question)
                else:
                    self.last_question = None
                    return NOT_A_QUESTION_RETURN
            else:
                parsed_question = ""
                args = []
                for keyword in question[:-1].split(' '):
                    try:
                        args.append(float(keyword))
                    except:
                        parsed_question += "{0} ".format(keyword)
                        if keyword in self.length_units or keyword in self.weight_units:
                            return self.unitcheck(keyword)
                parsed_question = parsed_question[0:-1]
                self.last_question = parsed_question
                for answer in self.question_answers.values():
                    if difflib.SequenceMatcher(a=answer.question, b=parsed_question).ratio() >= .90:
                        if answer.function is None:
                            return answer.value
                        else:
                            try:
                                if filepath != "":
                                    return answer.function(os.getcwd() + filepath)
                                else:
                                    return answer.function(*args)
                            except:
                                raise Exception("Too many extra parameters")
                else:
                    return UNKNOWN_QUESTION
                    
                    
    def conversion(self, question):
        main_digit = 0
        parsed_question = ""
        unit_1 = ""
        unit_2 = ""
        
        for keyword in question[::].split(' '):
            try:
                main_digit = float(keyword)
            except:
                parsed_question += "{0} ".format(keyword)
                
        for keyword in parsed_question[::].split(' '):
            if keyword in self.conversion_keywords:
                if unit_1 == "":
                    unit_1 = keyword
                else:
                    unit_2 = keyword

                

        if (unit_2 in self.weight_units and unit_1 in self.length_units) or (unit_1 in self.weight_units and unit_2 in self.length_units):
            return "Invalid conversion units"
            
        
        unit_1_val = self.conversion_keywords[unit_1]
        unit_2_val = self.conversion_keywords[unit_2]
        
        value = float(unit_1_val)/float(unit_2_val) * main_digit
        
        value = round(value, 3)
        
        stringval = str(value)
        
        if stringval[-1] == '0' and stringval [-2] == '.':
            stringval = str(value).rstrip('0').rstrip('.')
        
        return stringval + " " + unit_2
        
    def unitcheck(self, unit_input):
        print unit_input
        if unit_input in self.weight_units:
            return unit_input + " measure weight"
        elif unit_input in self.length_units:
            return unit_input + " measure length"

    def setuser(self, user_name):
        if not isinstance(user_name, str):
            return "Please enter a user name"
        else:
            self.username = user_name
            return "Username set."
            
    def haloutput(self):
        if self.username is None:
            return "No username set"
        else:
            return "I\'m afraid I can\'t do that " + self.username
            
    def teach(self, answer=""):
        if self.last_question is None:
            return NO_QUESTION
        elif self.last_question + " " in self.question_answers.keys():
            return NO_TEACH
        else:
            self.__add_answer(answer)
    def correct(self, answer=""):
        if self.last_question is None:
            return NO_QUESTION
        else:
            self.__add_answer(answer)
            
    def usernamecheck(self):
        if self.username is None:
            return "No username set"
        else:
            return self.username

    def __add_answer(self, answer):
        self.question_answers[self.last_question] = QA(self.last_question, answer)
