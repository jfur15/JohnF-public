from nose2.events import Plugin

Requirements = {}

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

class ReqPlugin(Plugin):
    configSection = 'req_tracer'
    commandLineSwitch = (None, 'req-tracer', 'Open file')
    
    def __init__(self):
        with open('Requirements.txt') as f:
            for line in f.readlines():
                if '#00' in line:
                    req_id, desc = line.split(' ', 1)
                    Requirements[req_id] = RequirementTrace(desc)

    def testOutcome(self, event):
        trace = open('traces.txt', 'w')
        for req in Requirements.keys():
            trace.write(req)
            trace.write(' - ')
            trace.write(str(Requirements[req].func_name))
            trace.write('\n')
