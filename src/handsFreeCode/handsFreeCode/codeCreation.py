import requests

def htmlify(str):
    return str.replace("\n", "<br/>").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")

def createFile(name):
    print("made file '" + name + "'")

def saveFile():
    print("save file")

def run():
    saveFile()
    pass

def appendLine(line):
    line = htmlify(line)
    r = requests.post('http://localhost:5000/append_line', data={"appendLine":line})

def deleteLine(lineNum):
    pass

def changeLine(lineNum, content):
    print(lineNum + " > " + content)

def showFile(filename):
    with open(filename) as f:
        for line in f.readlines():
            appendLine(line)
