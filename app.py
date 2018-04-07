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
def write_conditional(condition, if_true, if_false):
    print('condition:', condition)
    print('if_true:', if_true)
    print('if_false:', if_false)
    conditional_msg = render_template('conditional', condition=condition, if_true=if_true, if_false=if_false)
    return statement(conditional_msg)


# @ask.intent('')



if __name__ == '__main__':
    app.run(debug=True)
