# from src.CodeCreation.CodeCreation import *
# from handsFreeCode.handsFreeCode.handsFreeCode import *

output_path = './output/'

## most basic building block
class CodeLine:
    tab_level = 0
    line_string = ""
    keywords = []

    def __init__(self, line_string, keywords, tab_level=0):
        self.line_string = line_string
        self.keywords = keywords
        self.tab_level = tab_level

    def to_string(self):
        return ("\t" * self.tab_level) + self.line_string


# composed of other CodeBlocks or CodeLines
class CodeBlock:
    # code content may be either CodeBlock or CodeLine
    code_content = []
    # general tab level of code Block
    tab_level = 0
    # concatination of all keywords of all lines and sub-blocks
    keywords = []

    # def add_code(self, CodeBlock):


    def __init__(self, tabLevel=0):
        self.code_content = []
        self.tab_level = tabLevel
        self.keywords = []

    def flatten_to_codelines(self):
        print("Called flatten_to_codelines in CodeBlock.")
        newList = []
        for item in self.code_content:
            if type(item) is CodeLine:
                newList.append(item)
            else:
                newList.extend(item.flatten_to_codelines)
        return newList

    def flatten_keywords(self):
        newList = []
        for item in self.code_content:
            if type(item) is CodeLine:
                newList.extend(item.keywords)
            else:
                newList.extend(item.flatten_keywords)
        return newList

    def to_string(self):
        code_lines = self.flatten_to_codelines()
        return ''.join(line.to_string() for line in code_lines)



    def write_all(self):
        codeLines = self.flatten_to_codelines()
        for line in codeLines:
            print(line.to_string())
            # appendLine(line.to_string())

    # makes a while loop. takes exitCond:string, internal:codeBlock
    def make_me_a_loop(self, cond, internal=None):
        self.code_content.append(CodeLine("while " + cond + ":", ["loop"], self.tab_level))
        if internal:
            internal.tab_level += 1
            self.code_content.append(internal);

    def make_method_call(self, method_name, args=None, inline=None):
        str_args = ""
        if args:
            for i in range(len(args)):
                str_args += args[i]
                if i != len(args) - 1:
                    str_args += ", "
        res = CodeLine(method_name + "(" + str_args + ")", ["method_call"], self.tab_level)
        if inline:
            return res
        self.code_content.append(res)

    def make_me_a_print(self, varName):
        print(varName)
        self.code_content.append(CodeLine("print(" + varName + ")", ["print"], self.tab_level))

    def make_me_a_sort(self, listName):
        self.code_content.append(CodeLine(listName + " = sorted(" + listName + ")", ["sort", "list"], self.tab_level))

    def make_me_a_function(self, funName, args=None, internal=None):
        self.code_content.append(CodeLine("def " + funName + ','.join([str(a) for a in args] if args else "") + ":", ["function", funName], self.tab_level))
        if internal:
            internal.tab_level += 1
            self.code_content.append(internal)

    def create_a_var(self, name, val):
        self.code_content.append(CodeLine(name + " = " + val, ["var"], self.tab_level))

    # so what i need is an ifCondition and thenCode
    # optionally you can provide a list of elifConditions and elifThenCodes
    # --! but the list of elifThenCodes must be at most 1 longer than the list of elifConditions
    def make_me_a_conditional(self, ifCondition, thenCode, elifConditions, elifThenCodes):
        self.code_content.append(CodeLine("if " + ifCondition + " :", ["if"], self.tab_level))
        thenCode.tab_level += 1
        self.code_content.append(thenCode)
        if elifConditions :
            for elifCond, elifThenCode in zip(elifConditions, elifThenCodes):
                self.code_content.append(CodeLine("elif " + elifCond + ":", ["elif", "else if"], self.tab_level))
                elifThenCode.tab_level += 1
                self.code_content.append(elifThenCode)

            if len(elifThenCodes) > len(elifConditions):
                self.code_content.append(CodeLine("else: ", ["else"], self.tab_level))
                elifThenCodes[-1].tab_level += 1
                self.code_content.append(elifThenCodes[-1])


class Project:
    """A project"""
    name = ""
    command_queue = []
    used_function_names = []
    # bunch of code Blocks
    all_code = []

    def __init__(self, name):
        self.name = name
        self.command_queue = []
        self.used_function_names = []

        # Just to get rid of an error -- I think we need this!
        # createFile(name)

    def add_code(self, code):
        code.tab_level = 0
        self.all_code.append(code)

    def rem_code(self, keywords):
        pass

    def cha_code(self, keywords, newCode):
        pass

    def write_project_to_file(self):
        print('Writing everything to file %s' % self.name)
        output_file = open(output_path + self.name, 'w')

        for code in self.all_code:
            output_file.write(code.to_string())
            # print(code.get_codeblock_lines())
            output_file.close()

    def write_project_all(self):
        print("Called write_all in class project.")
        for code in self.all_code:
            code.write_all()
