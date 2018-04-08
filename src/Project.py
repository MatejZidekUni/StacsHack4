# from src.CodeCreation.CodeCreation import *
# from handsFreeCode.handsFreeCode.handsFreeCode import *

output_path = './output/'

# most basic building block
class CodeLine:
    tab_level = 0
    line_string = ""

    def __init__(self, line_string, tab_level=0):
        self.line_string = line_string
        self.tab_level = tab_level

    def to_string(self):
        print('tabs: %s' % ("\t" * self.tab_level))
        print('code: %s' % self.line_string)
        return str(("\t" * self.tab_level) + self.line_string)


# composed of other CodeBlocks or CodeLines
class CodeBlock:
    # code content may be either CodeBlock or CodeLine
    code_content = []
    # general tab level of code Block
    tab_level = 0
    # index of last used codeBlock
    last_codeBlock_index = -1

    def __init__(self, tabLevel=0):
        self.code_content = []
        self.tab_level = tabLevel

    def flatten_to_codelines(self):
        print("Called flatten_to_codelines in CodeBlock.")
        newList = []
        #if len(self.code_content) <= 0:
        #    self.code_content.append(CodeLine("pass", self.tab_level))

        for item in self.code_content:
            item.tab_level += self.tab_level
            if type(item) is CodeLine:
                print("-line- " + item.to_string() + " : " + str(item.tab_level))
                newList.append(item)
            else:
                newList.extend(item.flatten_to_codelines())
        return newList

    def to_string(self):
        code_lines = self.flatten_to_codelines()
        return '\n'.join(line.to_string() for line in code_lines)

    def write_all(self):
        codeLines = self.flatten_to_codelines()
        for line in codeLines:
            print(line.to_string())
            # appendLine(line.to_string())

    def add_code(self, codeBlock):
        print("codeBlock.addCode()")
        if(self.last_codeBlock_index >= 0):
            print("  go deeper")
            # increase tab level if we are going deeper in
            codeBlock.tab_level += 1
            if type(self.code_content[self.last_codeBlock_index]) == CodeBlock:
                self.code_content[self.last_codeBlock_index].add_code(codeBlock)
            else:
                self.code_content.append(codeBlock)
        else:
            print("  we are at tab level " + str(codeBlock.tab_level))
            self.code_content.append(codeBlock)
        self.last_codeBlock_index = self.code_content.index(codeBlock) # leave index on internal block


    # makes a while loop. takes exitCond:string, internal:codeBlock
    def make_me_a_loop_while(self, cond, internal=None):
        self.code_content.append(CodeLine("while " + cond + ":", self.tab_level))
        if internal is None:
            internal = CodeBlock(self.tab_level+1)
        else:
            internal.tab_level += self.tab_level
        self.code_content.append(internal)

        self.last_codeBlock_index = self.code_content.index(internal) # leave index on internal block

    # makes a while loop. takes exitCond:string, internal:codeBlock
    def make_me_a_loop_for(self, n, internal=None):
        self.code_content.append(CodeLine("for i in range(" + str(n) + "):", self.tab_level))
        if internal is None:
            internal = CodeBlock(self.tab_level + 1)
        else:
            internal.tab_level += self.tab_level
        self.code_content.append(internal)
        self.last_codeBlock_index = self.code_content.index(internal)  # leave index on internal block

    def make_me_a_print(self, whatever):
        self.code_content.append(CodeLine("print(" + whatever + ")", self.tab_level))

    def make_method_call(self, method_name, args=None, inline=None):
        str_args = ""
        if args:
            for i in range(len(args)):
                str_args += args[i]
                if i != len(args) - 1:
                    str_args += ", "
        res = CodeLine(method_name + "(" + str_args + ")", self.tab_level)
        if inline:
            return res
        self.code_content.append(res)

    def make_me_a_sort(self, listName):
        self.code_content.append(CodeLine(listName + " = sorted(" + listName + ")", self.tab_level))

    def make_me_a_function(self, funName, args=None, internal=None):
        self.code_content.append(CodeLine("def " + funName + "( "+ ','.join([str(a) for a in args] if args else "") + "):", self.tab_level))
        if internal:
            internal.tab_level += self.tab_level
        else:
            internal = CodeBlock(self.tab_level+1)
        self.code_content.append(internal)
        self.last_codeBlock_index = self.code_content.index(internal)  # leave index on internal block

    def create_a_var(self, name, val):
        self.code_content.append(CodeLine(name + " = " + val, self.tab_level))

    # so what i need is an ifCondition and thenCode
    # optionally you can provide a list of elifConditions and elifThenCodes
    # --! but the list of elifThenCodes must be at most 1 longer than the list of elifConditions
    def make_me_a_conditional(self, ifCondition, thenCode, elifConditions, elifThenCodes):
        self.code_content.append(CodeLine("if " + ifCondition + " :", self.tab_level))
        thenCode.tab_level += 1
        self.code_content.append(thenCode)
        if elifConditions:
            for elifCond, elifThenCode in zip(elifConditions, elifThenCodes):
                self.code_content.append(CodeLine("elif " + elifCond + ":", self.tab_level))
                elifThenCode.tab_level += self.tab_level
                self.code_content.append(elifThenCode)

            if len(elifThenCodes) > len(elifConditions) :
                self.code_content.append(CodeLine("else: ", self.tab_level))
                elifThenCodes[-1].tab_level += self.tab_level
                self.code_content.append(elifThenCodes[-1])

    def make_me_a_return(self, what=None):
        self.code_content.append(CodeLine("return " + what, self.tab_level))

class Project:
    """A project"""
    name = ""
    command_queue = []
    used_function_names = []
    # bunch of code Blocks
    all_code = []
    last_codeBlock_index = -1

    def __init__(self, name):
        self.name = name
        self.command_queue = []
        self.used_function_names = []

        # Just to get rid of an error -- I think we need this!
        # createFile(name)

    def add_code(self, code):
        code.tab_level = 0
        if(self.last_codeBlock_index > -1):
            print("going into codeBlock of project")
            self.all_code[self.last_codeBlock_index].add_code(code)
        else:
            self.all_code.append(code)
            self.last_codeBlock_index = self.all_code.index(code)

    def exit_codeBlock_one(self):
        # if our index is not -1
        if self.last_codeBlock_index != -1 :
            # if the index of the inner block is -1
            if self.all_code[self.last_codeBlock_index].last_codeBlock_index == -1:
                # then we progress to -1 too
                self.last_codeBlock_index = -1
            # else we move the inner block by 1
            else:
                self.all_code[self.last_codeBlock_index].exit_codeBlock_one()
        # else this shouldn't happen
        else:
            self.last_codeBlock_index = -2
        self.all_code[self.last_codeBlock_index].exit_codeBlock_one()

    def exit_codeBlock_all(self):
        self.last_codeBlock_index = -1

    def write_project_to_file(self):
        print('Writing everything to file %s' % self.name)
        output_file = open(output_path + self.name, 'w')

        for code in self.all_code:
            output_file.write(code.to_string())

        output_file.close()

    def write_project_all(self):
        print("Called write_all in class project.")
        for code in self.all_code:
            code.write_all()
