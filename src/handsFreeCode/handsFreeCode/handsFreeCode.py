import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
app = Flask(__name__)

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/code', methods=["GET"])
def show_code():
    return render_template('createdCode.html')

content = ""
def setCont(c):
    global content
    content = c

@app.route('/code', methods=["POST"])
def update_code():
    print(request.text)
    return render_template('createdCode.html')

@app.route('/get_buffered', methods=["GET"])
def get_buffered():
    return content

