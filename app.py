from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

# Local imports
from src.api import API

app = Flask(__name__)
ask = Ask(app, '/')
api_instance = API()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/code', methods=["GET"])
def get_code():
    return "Does this text get sent?"
    # return api_instance.write()


@ask.launch
def new_coding_session():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent('NewProjectIntent')
def new_project(project_name):
    new_project_msg = render_template('new_project', project_name=project_name)
    api_instance.new_project(project_name)
    return question(new_project_msg)


@ask.intent('FunctionIntent')
def new_function(func_name, arg_one, arg_two):
    # If the function takes in no arguments
    if arg_one is None and arg_two is None:
        new_func_msg = render_template('func_no_args', func_name=func_name)

    # If the function takes in one argument
    if arg_one is not None and arg_two is None:
        new_func_msg = render_template('func_one_arg', func_name=func_name, arg_one=arg_one)

    # If the function takes in two arguments
    if arg_one is not None and arg_two is not None:
        new_func_msg = render_template('func_two_args', func_name=func_name, arg_one=arg_one, arg_two=arg_two)

    return question(new_func_msg)

@ask.intent('ConditionalIntent')
def write_conditional(first_value, comparator, second_value, if_true, if_false):
    # If the conditional consists of two parts, e.g. 'if val == 1',
    # and there is no else block
    if comparator is not None and second_value is not None and if_false is None:
        conditional_msg = render_template('if_then', first_value=first_value, comparator=comparator, second_value=second_value, if_true=if_true)

    # If the conditional consists of two parts and there is an else block
    elif comparator is not None and second_value is not None and if_false is not None:
        conditional_msg = render_template('if_else', first_value=first_value, comparator=comparator, second_value=second_value, if_true=if_true, if_false=if_false)

    # If the conditional is just one part, e.g. 'if True' and there is no else block
    elif comparator is None and if_false is None:
        conditional_msg = render_template('if_then_short_conditional', first_value=first_value, if_true=if_true)

    # If the conditional is just one part and there is an else block
    else:
        conditional_msg = render_template('if_else_short_conditional', first_value=first_value, if_true=if_true, if_false=if_false)

    return question(conditional_msg)


@ask.intent("ProgramIntent")
def create_program(verb, name):
    print('program:', name)
    if name is None:
        # call without an optional argument name
        pass
    else:
        name = name + ".py"
    msg = render_template('program', prog_name=name)
    return question(msg)


@ask.intent("FunctionIntent")
def create_function(verb, name):
    print('function:', name)
    if name is None:
        # call without an optional argument name
        pass
    msg = render_template('function', func_name=name)
    return question(msg)


@ask.intent('WhileLoopIntent')
def while_loop(first_value, comparator, second_value, condition, boolean):
    if condition is not None and boolean is not None:
        boolean = True if boolean.lower() == "true" else False
        text = condition + " is " + str(boolean)
        while_msg = render_template('while', text=text)
    elif first_value is not None and comparator is not None and second_value is not None:
        text = first_value + " " + comparator + " " + second_value
        while_msg = render_template('while', text=text)
    return question(while_msg)


@ask.intent("MethodCallIntent")
def method_call(name, params):
    parameters = params.split(" and ")
    text = "parameters are: "
    for param in parameters:
        text += "'" + param + "'' "
    msg = render_template('method_call', name=name, params=text)
    return question(msg)


@ask.intent("PrintIntent")
def print_function(name, phrase, params):
    if phrase is not None and name is None and params is None:
        # print fixed phrase
        msg = render_template('printing', stuff=phrase)
    elif name is not None and phrase is None and params is None:
        # print result of a method call without parameters
        text = "the result of calling function '" + name + " without parameters"
        msg = render_template('printing', stuff=text)
    elif name is not None and params is not None and phrase is None :
        # print result of a method call with parameters
        parameters = params.split(" and ")
        text = "the result of calling function '" + name + " with parameters: "
        for param in parameters:
            text += "'" + param + "'' "
        msg = render_template('printing', stuff=text)
    return question(msg)

if __name__ == '__main__':
    app.run(debug=True)
