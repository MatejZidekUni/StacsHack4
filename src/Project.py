from src.CodeCreation.CodeCreation import *


class Project:
    """A project that is started"""
    name = ""
    command_queue = []
    used_function_names = []

    def __init__(self, name):
        self.name = name
        self.command_queue = []
        self.used_function_names = []

        createFile(name)
        saveFile()

    def change_function(self, name, content):
        pass