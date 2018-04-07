class Project:
    """A project that is started"""
    name = ""
    command_queue = []
    used_function_names = []

    def __init__(self, name):
        self.name = name
        self.command_queue = []
        self.used_function_names = []

    def new_function(self):
        pass