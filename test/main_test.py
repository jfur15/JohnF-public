"""
Test for source.main
"""
from source.main import Interface
from unittest import TestCase
import mock
from tests.plugins.ReqTracer import requirements, story
import math, time, subprocess, sys, os.path
import logging
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
    def test_measurement_job_story(self):
        self.assertEqual(mainAsk.ask("What unit do ounces measure?"), "ounces measure weight")
        
        self.assertEqual(mainAsk.ask("What unit do feet measure?"), "feet measure length")
    
class TestInherentCoverage(TestCase):
    def test_non_string_question(self):
        self.assertRaises(Exception, mainAsk.ask, 100)
        
    def test_functionless_answer(self):
        self.assertEqual(mainAsk.ask("Don't do anything"), "OK")
        
    def test_too_many_args(self):
        self.assertRaises(Exception, mainAsk.ask, "What is the square root of 10 and 20?")
    
    def test_no_set_username(self):
        self.assertEqual(mainAsk.setuser(10), "Please enter a user name")
        
    def test_cleared_username(self):
        mainAsk.ask("Please clear memory")
        self.assertEqual(mainAsk.ask("Open the door hal"), "No username set")
        
    def test_no_last_question(self):
        mainAsk.ask("Please clear memory")
        self.assertEqual(mainAsk.correct("Not an answer"), "Please ask a question first")
        
    def test_add_question(self):
        mainAsk.ask("Please clear memory")
        self.assertEqual(mainAsk.ask("What is the capital of Idaho?"), "I don't know, please provide the answer")
        mainAsk.correct("Boise")
        self.assertEqual(mainAsk.ask("What is the capital of Idaho?"), "Boise")
        
class GitCoverage(TestCase):
    @mock.patch('subprocess.Popen')
    def test_is_in_repo(self, m):
        process_mock = mock.Mock()
        attrs = {'communicate.return_value' : ('', '')}
        process_mock.configure_mock(**attrs)
        m.return_value = process_mock 

        self.assertEqual(mainAsk.ask("Is the " + os.getcwd() + "/test/main_test.py in the repo?"), "Yes")

    @mock.patch('subprocess.Popen')
    def test_is_untracked_in_repo(self, m):
        process_mock = mock.Mock()
        attrs = {'communicate.side_effect' : [('',''), ('',''), (os.getcwd() + '/test/main_test.pyc',''), ('','')]}
        process_mock.configure_mock(**attrs)
        m.return_value = process_mock 

        self.assertEqual(mainAsk.ask("Is the " + os.getcwd() + "/test/main_test.pyc in the repo?"), "No")

    @mock.patch('subprocess.Popen')
    def test_does_not_exist(self, m):
        process_mock = mock.Mock()
        attrs = {'communicate.return_value' : ('', '')}
        process_mock.configure_mock(**attrs)
        m.return_value = process_mock 

        self.assertEqual(mainAsk.ask("Is the /nonexistent.py in the repo?"), "No")
        
    @mock.patch('subprocess.Popen')
    def test_file_path_status_up_to_date(self, m):
        filepath = "/test/main_test.py"
        actualfile = "main_test.py"
        process_mock = mock.Mock()
        attrs = {'communicate.side_effect' : [ ("", ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''),('', ''),('', '')  ]}
        process_mock.configure_mock(**attrs)
        m.return_value = process_mock 

        self.assertEqual(mainAsk.ask("What is the status of " + os.getcwd() + filepath + "?"), actualfile + " is up to date")   
    
    @mock.patch('subprocess.Popen')
    def test_file_path_status_dirty_repo(self, m):
        filepath = "/test/main_test.py"
        actualfile = "main_test.py"
        process_mock = mock.Mock()
        attrs = {'communicate.side_effect' : [ ("", ''), ('', ''), ('', ''), (os.getcwd() + 'test/main_test.py', ''), ('', ''), (os.getcwd() + 'test/main_test.py', ''),('', ''),('', '')  ]}
        process_mock.configure_mock(**attrs)
        m.return_value = process_mock 

        self.assertEqual(mainAsk.ask("What is the status of " + os.getcwd() + filepath + "?"), actualfile + " is a dirty repo")   


    @mock.patch('subprocess.Popen')
    def test_file_path_status_not_checked(self, m):
        filepath = "/test/main_test.py"
        actualfile = "main_test.py"
        process_mock = mock.Mock()
        attrs = {'communicate.side_effect' : [ ("", ''), ('', ''), (os.getcwd() + '/test/main_test.py', ''), ('', ''), ('', ''), ('', ''),('', ''),('', '')  ]}
        process_mock.configure_mock(**attrs)
        m.return_value = process_mock 

        self.assertEqual(mainAsk.ask("What is the status of " + os.getcwd() + filepath + "?"), actualfile + " has been not been checked in")   

    @mock.patch('subprocess.Popen')
    def test_file_path_status_modified_locally(self, m):
        filepath = "/test/main_test.py"
        actualfile = "main_test.py"
        process_mock = mock.Mock()
        attrs = {'communicate.side_effect' : [ (os.getcwd() + "/test/main_test.py", ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''),('', ''),('', '')  ]}
        process_mock.configure_mock(**attrs)
        m.return_value = process_mock 

        self.assertEqual(mainAsk.ask("What is the status of " + os.getcwd() + filepath + "?"), actualfile + " has been modified locally")   

    @mock.patch('subprocess.Popen')
    def test_file_path_deal_with(self, m):
        filepath = "/test/main_test.py"
        actualfile = "main_test.py"
        fakestats = "6f697e8cb4cd1fakehash2e44813bf8ea9f65dcb, Wed Jan 24 08:00:00, jfur15"
        process_mock = mock.Mock()
        attrs = {'communicate.side_effect' : [ (fakestats, '') ]}
        process_mock.configure_mock(**attrs)
        m.return_value = process_mock 

        self.assertEqual(mainAsk.ask("What is the deal with " +  os.getcwd() + filepath + "?"), fakestats)   

    @mock.patch('subprocess.Popen')
    def test_file_path_repo_branch(self, m):
        filepath = "/test/main_test.py"
        actualfile = "main_test.py"
        process_mock = mock.Mock()
        attrs = {'communicate.side_effect' : [ ("branchname1", '') ]}
        process_mock.configure_mock(**attrs)
        m.return_value = process_mock 

        self.assertEqual(mainAsk.ask("What branch is " +  os.getcwd() + filepath + "?"), "branchname1")   
        
    @mock.patch('subprocess.Popen')
    def test_file_path_repo_url(self, m):
        filepath = "/test/main_test.py"
        actualfile = "main_test.py"
        process_mock = mock.Mock()
        attrs = {'communicate.side_effect' : [ ("https://github.com/OregonTech/repo1", '')  ]}
        process_mock.configure_mock(**attrs)
        m.return_value = process_mock 

        self.assertEqual(mainAsk.ask("Where did " +  os.getcwd() + filepath + " come from?"), "https://github.com/OregonTech/repo1")   
        
        
    @mock.patch('subprocess.Popen')
    def test_file_path_status_dirty_repo_untracked(self, m):
        filepath = "/test/main_test.py"
        actualfile = "main_test.py"
        process_mock = mock.Mock()
        attrs = {'communicate.side_effect' : [ ("", ''), ('', ''), ('', ''), ('', ''), ('', ''), ('main_test.py', ''),('', ''),('', '')  ]}
        process_mock.configure_mock(**attrs)
        m.return_value = process_mock 

        self.assertEqual(mainAsk.ask("What is the status of " + os.getcwd() + filepath + "?"), actualfile + " is a dirty repo")  
        

    @mock.patch('subprocess.Popen')
    def test_git_output_error(self, m):
        filepath = "/test/main_test.py"
        actualfile = "main_test.py"
        process_mock = mock.Mock()
        attrs = {'communicate.side_effect' : [ ("", 'AAA ERROR'), ('', ''), ('', ''), ('', ''), ('', ''), ('main_test.py', ''),('', ''),('', '')  ]}
        process_mock.configure_mock(**attrs)
        m.return_value = process_mock 

        self.assertEqual(mainAsk.ask("What is the status of " + os.getcwd() + filepath + "?"), actualfile + " is a dirty repo")  
        
        
    @mock.patch('subprocess.Popen')
    def test_git_execute_error(self, m):
        filepath = "/test/main_test.py"
        actualfile = "main_test.py"
        process_mock = mock.Mock()
        attrs = {'communicate.side_effect' : [ ("", 'AAA ERROR'), ('', ''), ('', ''), ('', ''), ('', ''), ('main_test.py', ''),('', ''),('', '')  ]}
        process_mock.configure_mock(**attrs)
        m.return_value = process_mock 

        with self.assertRaises(Exception):
            mainAsk.ask("What is the status of " + filepath + "?")  
        
    def test_file_check_valid_path(self):
        with self.assertRaises(Exception):
            mainAsk.ask("What is the status of /uuugarbaggeu##/*#/.#?")

class PerformanceTests(TestCase):
    @requirements(['#0051']) 
    def test_perf_basic_question(self):
        start = time.time()
        mainAsk.ask("What time is it?")
        end = time.time()
        print end-start
        self.assertTrue(end-start <= .05)
        
    @requirements(['#0051']) 
    def test_perf_question_without_answer(self):
        start = time.time()
        mainAsk.ask("Please clear memory")
        end = time.time()
        print end-start
        self.assertTrue(end-start <= .05)
        
    @requirements(['#0051']) 
    def test_perf_small_complex_question(self):
        start = time.time()
        mainAsk.ask("Convert 200 pounds to ounces")
        end = time.time()
        print end-start
        self.assertTrue(end-start <= .05)
        
    @requirements(['#0051']) 
    def test_perf_larger_question(self):
        start = time.time()
        mainAsk.ask("What is digit 10 of fibonacci?")
        end = time.time()
        print end-start
        self.assertTrue(end-start <= .05)
        
    @requirements(['#0051']) 
    def test_perf_improbable_question(self):
        start = time.time()
        mainAsk.ask("What is digit 20 of fibonacci?")
        end = time.time()
        print end-start
        self.assertTrue(end-start <= .05)
