"""
successful commands are pushed to the command_queue
if no names are supplied to new projects, functions then random names are generated
else  the given name will be used. if the given name is already allocated, then throw err
"""

from random import randint
from src.Project import Project
from src.CodeCreation.CodeCreation import *

command_queue = []
sample_names = ["foo", "sock", "flow", "cool", "martini", "stuff", "example", "test", "code", "love", "banana"]

used_project_names = []
projects = []
cur_project_index = -1


def gen_name(name, used):
    if name and name not in used:
        return name
    elif name:
        return None
    else:
        n = sample_names[randint(0, len(sample_names)-1)]
        while n in used:
            n += "_" + sample_names[randint(0, len(sample_names)-1)]
        return n


# start new project
# id 0
# returns err string if err, otherwise returns None
def newProject(name):
    name = gen_name(name, used_project_names)
    if name is None:
        return "Can you choose another name?"
    projects.append(Project(name))
    cur_project_index += 1
    command_queue.insert(0, 0)
    return None

def newFunction(name, args):
    command_queue.insert(0, 1)
    # append new line
    # add "def name:"


def newCondition(if_, then_, else_):
    command_queue.insert(0, 2)

def newLoop(breakCond, loopN):
    command_queue.insert(0, 3)

def fillLoop(statements):
    command_queue.insert(0, 4)

def takeInput():
    command_queue.insert(0, 5)

def produceOutput():
    command_queue.insert(0, 6)
