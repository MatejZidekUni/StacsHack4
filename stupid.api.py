from random import randint


command_queue = []
sample_names = ["foo", "sock", "flow", "cool", "martini", "stuff", "example", "test", "code", "love", "banana"]

used_project_names = []
projects = []

def gen_name(name):
    if name and name not in used_project_names :
        return name
    elif name :
        return None
    else :
        n = sample_names[randint(0, len(sample_names)-1)]
        while n in used_project_names :
            n += "_" + sample_names[randint(0, len(sample_names)-1)]
        return n


# start new project
# id 0
# returns err string if err, otherwise returns None
def newProject(name):
    commandQueue.insert(0, 0)
    name = gen_name(name)
    if name is None:
        return "Can you choose another name?"
    projects.append(Project(name))
    return None

def newFunction(name, args):
    commandQueue.insert(0, 1)

def newCondition(if_, then_, else_):
    commandQueue.insert(0, 2)

def newLoop(breakCond, loopN):
    commandQueue.insert(0, 3)

def fillLoop(statements):
    commandQueue.insert(0, 4)

def takeInput():
    commandQueue.insert(0, 5)

def produceOutput():
    commandQueue.insert(0, 6)
