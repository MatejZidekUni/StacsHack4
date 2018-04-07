from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import random

app = Flask(__name__)
ask = Ask(app, '/')

TAB_STR = '    '

@ask.launch
def new_coding_session():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent('ConditionalIntent')
def write_conditional(condition, if_true, if_false):
    if if_false is not None:
        code_lines = [0] * 4
        code_lines[0] = 'if ' + condition + ':'
        code_lines[1] = TAB_STR + if_true
        code_lines[2] = 'else:'
        code_lines[3] = TAB_STR + if_false

        conditional_msg = render_template('if_else', condition=condition, if_true=if_true, if_false=if_false)
    else:
        code_lines = [0] * 2
        code_lines[0] = 'if ' + condition + ':'
        code_lines[1] = TAB_STR + if_true
        conditional_msg = render_template('if_then', condition=condition, if_true=if_true)

    print('\n' + '\n'.join(code_lines) + '\n')
    return question(conditional_msg)


@ask.intent('WhileLoopIntent')



@ask.intent("ProgramIntent")
def create_program(verb, name):
    print('program:', name)
    msg = render_template('program', prog_name=name)
    return question(msg)

if __name__ == '__main__':
    app.run(debug=True)
