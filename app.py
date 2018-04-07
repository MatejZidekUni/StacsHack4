from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def new_coding_session():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


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


@ask.intent('ClassIntent')
def write_class(class_name, property_one, property_two):
    # If no properties have been given
    if property_one is None and property_two is None:
        class_msg = render_template('class_no_props', class_name=class_name)

    # If just one property has been given
    elif property_two is None:
        class_msg = render_template('class_one_prop', class_name=class_name, property_one=property_one)

    # If


@ask.intent('ProgramIntent')
def create_program(verb, name):
    print('program:', name)
    msg = render_template('program', prog_name=name)
    return question(msg)

if __name__ == '__main__':
    app.run(debug=True)
