"""
Test for source.main
"""
from source.main import Interface
from unittest import TestCase
from tests.plugins.ReqTracer import requirements, story
import math, time
mainAsk = Interface()

class TestQuestionSyntax(TestCase):
    @requirements(['#0006'])
    def test_question_input(self):
        self.assertTrue(isinstance(mainAsk.ask("Input"), str))
        
    @requirements(['#0007'])
    def test_question_input_how(self):
        self.assertTrue(isinstance(mainAsk.ask("How does this work?"), str))
    @requirements(['#0007'])
    def test_question_input_what(self):
        self.assertTrue(isinstance(mainAsk.ask("What does this work?"), str))
    @requirements(['#0007'])
    def test_question_input_where(self):
        self.assertTrue(isinstance(mainAsk.ask("Where does this work?"), str))
    @requirements(['#0007'])
    def test_question_input_why(self):
        self.assertTrue(isinstance(mainAsk.ask("Why does this work?"), str))
    @requirements(['#0007'])
    def test_question_input_who(self):
        self.assertTrue(isinstance(mainAsk.ask("Who does this work?"), str))

    @requirements(['#0008'])
    def test_no_question_keyword(self):
        answer = "Was that a question?"
        self.assertEqual(mainAsk.ask("Not a question?"), answer)
        
    @requirements(['#0009'])
    def test_no_question_mark(self):
        answer = "Was that a question?"
        self.assertEqual(mainAsk.ask("How is this a question"), answer)

class TestQuestionDeterminingAnswers(TestCase):
    @requirements(['#0010'])
    def test_question_spaces(self):
        answer = "I don't know, please provide the answer"
        self.assertEqual(mainAsk.ask("How does this work?"), answer)
        self.assertFalse(mainAsk.ask("Howdoesthiswork?") == answer)
        
    @requirements(['#0011'])
    def test_question_keywords(self):
        self.assertEqual(mainAsk.ask("What type triangle is 1 1 1?"), "equilateral")
        
        self.assertNotEqual(mainAsk.ask("What triangle is 1 1 1?"), "equilateral")
        
    @requirements(['#0012']) 
    def test_question_function_input(self):
        self.assertEqual(mainAsk.ask("What type of triangle is 1 2 1?"), "isosceles")
        
        
    @requirements(['#0013']) 
    def test_question_function_answer(self):
        self.assertEqual(mainAsk.ask("What type of quadrilateral is 1 2 1 2?"), "rectangle")
        
    @requirements(['#0014']) 
    def test_question_function_no_match(self):
        answer = "I don't know, please provide the answer"  
        self.assertEqual(mainAsk.ask("What type of sphere is 1 1 1?"), answer)
        
class TestQuestionProvidingAnswers(TestCase):
    @requirements(['#0015'])
    def test_question_teaching(self):
        mainAsk.ask("What comes after 1?")
        mainAsk.teach("2")
        self.assertEqual(mainAsk.ask("What comes after 1?"), "2")
        
    @requirements(['#0016'])
    def test_question_function_teaching(self):
        funct = math.factorial
        mainAsk.ask("What is the factorial of 4?")
        mainAsk.teach(funct)
        self.assertEqual(mainAsk.ask("What is the factorial of 4?"), math.factorial(4))

    @requirements(['#0017'])
    def test_question_teaching_none(self):
        mainAsk.ask("Not a question")
        self.assertEqual(mainAsk.teach("No it isn't"), "Please ask a question first")
    
    @requirements(['#0018'])
    def test_question_teaching_refuse(self):
        self.assertEqual(mainAsk.ask("What type of triangle is 1 1 1?"), "equilateral")
        self.assertEqual(mainAsk.teach("not"), "I don\'t know about that. I was taught differently")

class TestQuestionCorrectingAnswers(TestCase):
    @requirements(['#0019'])
    def test_question_updating(self):
        mainAsk.ask("What comes after 1?")
        mainAsk.teach("two")
        self.assertEqual(mainAsk.ask("What comes after 1?"), "two")
        
    @requirements(['#0020'])
    def test_question_correcting_teaching(self):
        funct = math.factorial
        mainAsk.ask("What is the factorial of 4?")
        mainAsk.teach(funct)
        self.assertEqual(mainAsk.ask("What is the factorial of 4?"), math.factorial(4))

    @requirements(['#0021'])
    def test_question_correcting_none(self):
        mainAsk.ask("Not a question")
        self.assertEqual(mainAsk.teach("No it isn't"), "Please ask a question first")
    
class JobStories(TestCase):
    @story(['When I ask "What time is it?" I want to be given the current date/time so I can stay up to date'])
    def test_time_job_story(self):
        self.assertEqual(mainAsk.ask("What time is it?"), time.strftime("%c"))

    @story(['When I ask "What is the n digit of fibonacci" I want to receive the answer so I don\'t have to figure it out myself'])
    def test_fibo_job_story(self):
        self.assertEqual(mainAsk.ask("What is digit 10 of fibonacci?"), 55)

    @story(['When I ask "What is the n digit of pi" I want to receive the answer so I don\'t have to figure it out myself'])
    def test_pi_job_story(self):
        self.assertEqual(mainAsk.ask("What is digit 1 of pi?"), '3')
    
    @story(['When I say "Open the door hal", I want the application to say "I\'m afraid I can\'t do that (user name) so I know that is not an option'])
    def test_open_door_user_job_story(self):
        name = "Dave"
        mainAsk.setuser(name)
        self.assertEqual(mainAsk.ask("Open the door hal"), "I\'m afraid I can\'t do that "+ name)
        
    @story(['When I ask "Please clear memory" I was the application to clear user set questions and answers so I can reset the application'])
    def test_memory_job_story(self):
        funct = math.factorial
        mainAsk.ask("What is the factorial of 4?")
        mainAsk.teach(funct)
        mainAsk.ask("Please clear memory")
        self.assertEqual(mainAsk.ask("What is the factorial of 4?"), "I don't know, please provide the answer")
        
    @story(['When I ask "Convert <number> <units> to <units>" I want to receive the converted value and units so I can know the answer.','When I ask for a numberic conversion I want at least 10 different units I can convert from/to'])
    def test_converted_value_job_story(self):
        self.assertEqual(mainAsk.ask("Convert 10 pounds to ounces"), '160 ounces')
        self.assertEqual(mainAsk.ask("Convert 20 ounces to pounds"), '1.25 pounds')
        self.assertEqual(mainAsk.ask("Convert 40 feet to inches"), '480 inches')
        self.assertEqual(mainAsk.ask("Convert 24 inches to feet"), '2 feet')
        self.assertEqual(mainAsk.ask("Convert 100 centimeters to meters"), '1 meters')
        self.assertEqual(mainAsk.ask("Convert 10 meters to centimeters"), '1000 centimeters')
        self.assertEqual(mainAsk.ask("Convert 500 yards to miles"), '0.284 miles')
        self.assertEqual(mainAsk.ask("Convert 10 miles to yards"), '17600 yards')
        self.assertEqual(mainAsk.ask("Convert 10 grams to kilograms"), '0.1 kilograms')
        self.assertEqual(mainAsk.ask("Convert 10 kilograms to grams"), '1000 grams')
        self.assertEqual(mainAsk.ask("Convert 50 inches to grams"), "Invalid conversion units")

    @story(['When I ask "What is the square root of x" I want to recieve the answer so I don\'t have to figure it out myself'])
    def test_square_root_job_story(self):
        self.assertEqual(mainAsk.ask("What is the square root of 4?"), "2.0")
        
    @story(['When I ask "When is the next leap year" I want to receive the answer of the date'])
    def test_leap_year_job_story(self):
        self.assertEqual(mainAsk.ask("What is the next leap year?"), "2020")
        
    @story(['When I ask "What is my username" I want to receieve an answer or an error'])
    def test_username_job_story(self):
        mainAsk.ask("Please clear memory")
        self.assertEqual(mainAsk.ask("What is my username?"), "No username set")
        mainAsk.setuser("John")
        self.assertEqual(mainAsk.ask("What is my username?"), "John")
        
    @story(['When I ask "What is the cube root of x", I want to receive the answer rounded to 3 decimal places'])
    def test_cube_root_job_story(self):
        self.assertEqual(mainAsk.ask("What is the cubic root of 10?"), "2.154")

    @story(['When I ask "What do ____ measure", I want to know what the unit measures'])
    def test_cube_root_job_story(self):
        self.assertEqual(mainAsk.ask("What do ounces measure?"), "ounces measure weight")
        
        self.assertEqual(mainAsk.ask("What do feet measure?"), "feet measure length")
    
