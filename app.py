from flask import Flask, render_template, url_for
from flask_ask import Ask, statement, question, session

# Local imports
from src.api import API

app = Flask(__name__)
ask = Ask(app, '/')
api_instance = API()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/code')
def get_code():
    return "Does this text get sent?"
    # return api_instance.write()

@ask.launch
def new_coding_session():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("ProgramIntent")
def create_program(verb, name):
    print('program:', name)
    if name is None:
        # Call without an optional argument name
        api_instance.new_project()
    else:
        name = name + ".py"
        api_instance.new_project(name=name)

    api_instance.write_to_file()
    msg = render_template('program', prog_name=name)
    return question(msg)


@ask.intent('FunctionIntent')
def new_function(_, name, params):
    if params is None:
        # If the function takes in no arguments
        if name is None:
            api_instance.new_function()
        api_instance.new_function(name=name)
        new_func_msg = render_template('func_no_args', func_name=name)
    else:
        text = " with parameters: "
        parameters = params.split(" and ")
        for p in parameters:
            parameters.append(p)
            text += "'" + p + "' "
        if name is None:
            api_instance.new_function(args=parameters)
        api_instance.new_function(name=name, args=parameters)
        new_func_msg = render_template('func_with_args', func_name=name, text=text)
    return question(new_func_msg)


@ask.intent('ConditionalIntent')
def write_conditional(first_value, comparator, second_value, if_true, if_false):
    # If the conditional consists of two parts, e.g. 'if val == 1',
    # and there is no else block
    if comparator is not None and second_value is not None and if_false is None:
        conditional_msg = render_template('if_then', first_value=first_value, comparator=comparator, second_value=second_value, if_true=if_true)
        cond = first_value + " " + sign(comparator) + " " + second_value
        api_instance.new_condition(cond, if_true, None, None)
    # If the conditional consists of two parts and there is an else block
    elif comparator is not None and second_value is not None and if_false is not None:
        conditional_msg = render_template('if_else', first_value=first_value, comparator=comparator, second_value=second_value, if_true=if_true, if_false=if_false)
        cond = first_value + " " + sign(comparator) + " " + second_value
        api_instance.new_condition(cond, if_true, [], [if_false])
    # If the conditional is just one part, e.g. 'if True' and there is no else block
    elif comparator is None and if_false is None:
        conditional_msg = render_template('if_then_short_conditional', first_value=first_value, if_true=if_true)
        api_instance.new_condition(first_value, if_true, None, None)
    # If the conditional is just one part and there is an else block
    else:
        conditional_msg = render_template('if_else_short_conditional', first_value=first_value, if_true=if_true, if_false=if_false)
        api_instance.new_condition(first_value, if_true, [], [if_false])
    return question(conditional_msg)


@ask.intent('WhileLoopIntent')
def while_loop(first_value, comparator, second_value, condition, boolean):
    if condition is not None and boolean is not None:
        boolean = True if boolean.lower() == "true" else False
        text = condition + " is " + str(boolean)
        while_msg = render_template('while', text=text)
        cond = first_value + " is " + str(boolean)
    elif first_value is not None and comparator is not None and second_value is not None:
        text = first_value + " " + comparator + " " + second_value
        while_msg = render_template('while', text=text)
        cond = first_value + " " + sign(comparator) + " " + second_value
    api_instance.new_loop_while(cond)
    return question(while_msg)


@ask.intent("MethodCallIntent")
def method_call(name, params):
    if not params:
        api_instance.call_method(name)
    else:
        parameters = params.split(" and ")
        text = "parameters are: "
        for param in parameters:
            text += "'" + param + "'' "
        api_instance.call_method(name, args=parameters)
    msg = render_template('method_call', name=name, params=text)
    return question(msg)


@ask.intent("PrintIntent")
def print_function(name, phrase, params):
    if phrase is not None and name is None and params is None:
        # print fixed phrase
        api_instance.produce_output(phrase)
        msg = render_template('printing', stuff=phrase)
    elif name is not None and phrase is None and params is None:
        # print result of a method call without parameters
        text = "the result of calling function '" + name + " without parameters"
        res = api_instance.call_method(name, inline=True)
        api_instance.produce_output(res)
        msg = render_template('printing', stuff=text)
    elif name is not None and params is not None and phrase is None:
        # print result of a method call with parameters
        parameters = params.split(" and ")
        text = "the result of calling function '" + name + " with parameters: "
        for param in parameters:
            text += "'" + param + "' "
        msg = render_template('printing', stuff=text)
        res = api_instance.call_method(name, args=parameters, inline=True)
        api_instance.produce_output(res)
    return question(msg)


@ask.intent("CreateVarIntent")
def create_var(name, function, value, params):
    if name is not None and value is not None:
        api_instance.create_variable(name, value)
        msg = render_template('variable', value=value)
        return question(msg)
    if params is None:
        method = api_instance.call_method(name, inline=True)
        api_instance.create_variable(name, method)
    else:
        parameters = params.split(" and ")
        method = api_instance.call_method(name, parameters, inline=True)
        api_instance.create_variable(name, method)


@ask.intent("ReturnIntent")
def create_var(name, text):
    if name is not None:
        api_instance.return_something(name)
    elif text is not None:
        api_instance.return_something(text)

@ask.intent("ExitIntent")
def exit_function(reason):
    api_instance.jump_up_1()


dict = {
    "greater than or equals": ">=",
    "less than or equals": ">=",
    "greater than": ">",
    "less than": "<",
    "equals": "==",
    "is": "==",
    "has": "contains",
}


def sign(comparator):
    if comparator in dict:
        return dict[comparator]
    return comparator


if __name__ == '__main__':
    app.run(debug=True)
