from copy import deepcopy

from flask import Flask, request, render_template, jsonify
app = Flask(__name__)

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('HFC_SETTINGS', silent=True)

content = {"appendLines":[], #[content1, content2,...]
           "changeLines":[], #[(lineNum, newCont),...]
           "insertLines":[], #[(lineNum, content),...]
           "deleteLines":[], #[lineNum1, lineNum2,...]
           "mkFile": False,
           "delFile": False,
           "saveFile": False,
           "run": False,
           "hasChanged":False
           }
contentFresh = deepcopy(content)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/code', methods=["GET"])
def show_code():
    return render_template('createdCode.html')

@app.route('/get_new_cont', methods=["GET"])
def get_new_cont():
    global content
    json = jsonify(content)
    content = deepcopy(contentFresh)
    return json

@app.route('/append_line', methods=["POST"])
def append_line():
    line = request.form.get("appendLine")
    content["appendLines"].append(line)
    content["hasChanged"] = True
    return line