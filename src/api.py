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
        self.write_to_file()

    # basically moves the requested project back to the front of the project list
    # id 0.1
    def switch_project(self, name):
        if name not in self.used_project_names:
            return "You don't have a project with that name yet"
        proj_i = self.project_stack.index([elem for elem in self.project_stack if elem.name == name])
        proj = self.project_stack.pop(proj_i)
        self.project_stack.insert(0, proj)

    # creates new function
    # uses last project created or creates new project if none available
    def new_function(self, name=None, args=None):
        if len(self.project_stack) <= 0:
            self.new_project()

        name = self.gen_name(name, self.project_stack[0].used_function_names)

        the_code = CodeBlock()
        the_code.make_me_a_function(name, args)
        self.project_stack[0].add_code(the_code)
        self.project_stack[0].used_function_names.append(name)
        self.project_stack[0].write_project_to_file()

        self.write()

    def jump_up_1(self):
        if len(self.project_stack) <= 0:
            self.new_project()
        self.project_stack[0].exit_codeBlock_one()

    def jump_up_all(self):
        if len(self.project_stack) <= 0:
            self.new_project()
        self.project_stack[0].exit_codeBlock_all()

    def new_condition(self, ifCondition, thenCode, elifConditions, elifThenCodes):
        if len(self.project_stack) <= 0:
            self.new_project()

        the_code = CodeBlock()
        thenCode = CodeLine(the_code.to_string(), the_code.tab_level)
        the_code.make_me_a_conditional(ifCondition, thenCode, elifConditions, elifThenCodes)
        self.project_stack[0].add_code(the_code)
        self.project_stack[0].write_project_to_file()

        self.write()

    def new_loop_while(self, cond, internal=None):
        the_code = CodeBlock()
        internal = CodeLine(the_code, the_code.tab_level)
        if internal:
            the_code.make_me_a_loop_while(cond, internal)
        else:
            the_code.make_me_a_loop_while(cond)
        self.project_stack[0].add_code(the_code)
        self.write()

    def new_loop_for(self, n, internal=None):
        the_code = CodeBlock()
        the_code.make_me_a_loop_for(n, internal)
        self.project_stack[0].add_code(the_code)
        self.project_stack[0].write_project_to_file()
        self.write()

    def fill_loop(self, internal):
        if len(self.project_stack) <= 0:
            print("NO LOOP to fill")
            return None
        self.project_stack[0].add_code(internal)
        self.project_stack[0].write_project_to_file()
        self.write()

    def produce_output(self, whatever):
        the_code = CodeBlock()
        if len(self.project_stack) <= 0:
            self.new_project()
        if type(whatever) is CodeLine:
            whatever = whatever.to_string()
        the_code.make_me_a_print(whatever)
        self.project_stack[0].add_code(the_code)
        self.project_stack[0].write_project_to_file()
        self.write()

    def return_something(self, what_to_return):
        the_code = CodeBlock()
        if len(self.project_stack) <= 0:
            self.new_project()
        if type(what_to_return) is CodeLine:
            what_to_return = what_to_return.to_string()

        the_code.make_me_a_return(what_to_return)

        self.project_stack[0].add_code(the_code)
        self.project_stack[0].write_project_to_file()
        self.write()

    def call_method(self, name, args=None, inline=None):
        the_code = CodeBlock()
        if len(self.project_stack) <= 0:
            self.new_project()
        res = the_code.make_method_call(name, args, inline=inline)
        if not inline:
            self.project_stack[0].add_code(the_code)
            self.project_stack[0].write_project_to_file()
            self.write()
        else:
            return res

    def create_variable(self, name, value):
        the_code = CodeBlock()
        if len(self.project_stack) <= 0:
            self.new_project()
        the_code.create_a_var(name, value)
        self.project_stack[0].add_code(the_code)
        self.project_stack[0].write_project_to_file()
        self.write()

    def write(self):
        print("API: called write")
        if len(self.project_stack) <= 0:
            self.new_project()
        self.project_stack[0].write_project_all()

    def write_to_file(self):
        print("API: writing to file.")
        if len(self.project_stack) <= 0:
            self.new_project()
        self.project_stack[0].write_project_to_file()
