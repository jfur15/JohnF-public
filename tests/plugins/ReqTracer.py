from nose2.events import Plugin
import string
Requirements = {}
Stories = {}
class RequirementTrace(object):
    req_text = ""
    def __init__(self, text):
        self.req_text = text
        self.func_name = []

def requirements(req_list):
    def wrapper(func):
        def add_req_and_call(*args, **kwargs):
            for req in req_list:
                if req not in Requirements.keys():
                    raise Exception('Requirement {0} not defined'.format(req))
                Requirements[req].func_name.append(func.__name__)
            return func(*args, **kwargs)

        return add_req_and_call

    return wrapper

def story(story_list):
    def wrapper(func):
        def add_req_and_call(*args, **kwargs):
            for story_input in story_list:
                if story_input not in Stories:
                    raise Exception('This story: \n\n {0} \n\n is not defined'.format(story_input))
                Stories[story_input].func_name = (func.__name__)
            return func(*args, **kwargs)

        return add_req_and_call

    return wrapper



class ReqPlugin(Plugin):
    configSection = 'req_tracer'
    commandLineSwitch = (None, 'req-tracer', 'Open file')
    
    def __init__(self):
        with open('Requirements.txt') as f:
            for line in f.readlines():
                if '#00' in line:
                    req_id, desc = line.split(' ', 1)
                    Requirements[req_id] = RequirementTrace(desc)
                if '*' in line:
                    storydesc = line.strip('*\n')
                    storytrace = RequirementTrace(storydesc)
                    Stories[storydesc] = storytrace

    def testOutcome(self, event):
        trace = open('traces.txt', 'w')
        for req in Requirements.keys():
            trace.write(req)
            trace.write(' - ')
            trace.write(str(Requirements[req].func_name))
            trace.write('\n')
        for story in Stories.keys():
            trace.write(story)
            trace.write('\n')
            trace.write(str(Stories[story].func_name))
            trace.write('\n\n')
