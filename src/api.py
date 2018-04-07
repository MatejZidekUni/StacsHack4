"""
    successful commands are pushed to the command_queueue
    if no names are supplied to new projects, functions then random names are generated
    else  the given name will be used. if the given name is already allocated, then throw err

    ids:
    0.0 make new project
    0.1 switch to project
    0.2 scrap project
    1.0 make new function
    1.1 switch to function
    1.2 scrap function
"""

from random import randint
from src.Project import *
from src.CodeCreation.CodeCreation import *

class API:
    command_queue = []
    sample_names = ["foo", "sock", "flow", "cool", "martini", "stuff", "example", "test", "code", "love", "banana"]

    used_project_names = []
    project_stack = []

    def __init__(self):
        self.command_queue = []
        self.used_project_names = []
        self.project_stack = []

    def gen_name(self, name, used):
        if name and name not in used:
            return name
        elif name:
            return None
        else:
            n = self.sample_names[randint(0, len(self.sample_names)-1)]
            while n in used:
                n += "_" + self.sample_names[randint(0, len(self.sample_names)-1)]
            return n

    def done(self, id):
        self.command_queue.insert(0, id)
        print("completed command : " + str(id))
        return None

    ## ---------------------------------------------------------------------

    # make new project
    # id 0.0
    # returns err string if err, otherwise returns None
    def new_project(self, name=None):
        name = self.gen_name(name, self.used_project_names)
        if name is None:
            return "You have used that name before"
        self.project_stack.insert(0, Project(name))
        self.used_project_names.append(name)
        return self.done(0.0)

    # basically moves the requested project back to the front of the project list
    # id 0.1
    def switch_project(self, name):
        if name not in self.used_project_names:
            return "You don't have a project with that name yet"
        proj_i = self.project_stack.index([elem for elem in self.project_stack if elem.name == name])
        proj = self.project_stack.pop(proj_i)
        self.project_stack.insert(0, proj)
        return self.done(0.1)


    # creates new function
    # uses last project created or creates new project if none available
    def new_function(self, name=None, args=None):
        if len(self.project_stack) <= 0:
            self.new_project()

        name = self.gen_name(name, self.used_project_names) #todo

        the_code = CodeBlock()
        the_code.make_me_a_function(name, args)
        self.project_stack[0].add_code(the_code)

        self.done(1.0)


    def new_condition(self, if_, then_, else_):
        self.command_queue.insert(0, 2)

    def new_loop(self, breakCond, loopN):
        self.command_queue.insert(0, 3)

    def fill_loop(self, statements):
        self.command_queue.insert(0, 4)

    def take_input(self):
        self.command_queue.insert(0, 5)

    def produce_output(self):
        self.command_queue.insert(0, 6)

    def write(self):
        if len(self.project_stack) <= 0:
            self.new_project()
        self.project_stack[0].write_all()
        self.done(10.0)
