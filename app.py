from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import random

app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def new_coding_session():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent('ConditionalIntent')
def write_conditional(first_value, comparator, second_value, if_true, if_false):
    # If the conditional is in two parts, e.g. 'if val == 1'
    if comparator is not None and second_value is not None:
        # If there is an else block
        if if_false is not None:
            conditional_msg = render_template('if_else', first_value=first_value,
                comparator=comparator, second_value=second_value, if_true=if_true,
                if_false=if_false)
        # If there is no else block
        else:
            conditional_msg = render_template('if_then', first_value=first_value,
            comparator=comparator, second_value=second_value, if_true=if_true)

    # If the conditional is just one part, e.g. 'if True'
    else:
        # If there is an else block
        if if_false is not None:
            conditional_msg = render_template('if_else_short_conditional', first_value=first_value, comparator=comparator, second_value=second_value, if_true=if_true, if_false=if_false)
        # If there is no else block
        else:
            conditional_msg = render_template('if_then_short_conditional', first_value=first_value, comparator=comparator, second_value=second_value, if_true=if_true)

    return question(conditional_msg)


@ask.intent('WhileLoopIntent')



@ask.intent("ProgramIntent")
def create_program(verb, name):
    print('program:', name)
    msg = render_template('program', prog_name=name)
    return question(msg)

if __name__ == '__main__':
    app.run(debug=True)
