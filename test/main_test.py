"""
Test for source.main
"""
from source.main import Interface
from unittest import TestCase
from tests.plugins.ReqTracer import requirements
import math
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
    def test_question_teaching_none(self):
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
    
