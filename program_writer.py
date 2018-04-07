import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("ProgramIntent")
def answer(verb, name):
    return statement(msg)


if __name__ == '__main__':
    app.run(debug=True)
